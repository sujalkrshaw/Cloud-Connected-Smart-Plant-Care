from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from .config import settings
from .models import Device, SensorReading, WateringEvent, Alert

PLANT_PROFILES = {
    'succulent': {'threshold': 20.0},
    'tomato': {'threshold': 40.0},
    'herb': {'threshold': 35.0},
    'indoor': {'threshold': 30.0},
}

def now_utc():
    return datetime.now(timezone.utc)

def as_utc(dt):
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

def add_alert(db: Session, device_id: str, alert_type: str, level: str, message: str):
    existing = db.query(Alert).filter(Alert.device_id == device_id, Alert.alert_type == alert_type, Alert.status == 'OPEN').first()
    if existing:
        return existing
    alert = Alert(alert_id=f'ALT-{uuid4().hex[:10].upper()}', device_id=device_id, alert_type=alert_type, level=level, message=message)
    db.add(alert)
    return alert

def resolve_alert(db: Session, device_id: str, alert_type: str):
    for alert in db.query(Alert).filter(Alert.device_id == device_id, Alert.alert_type == alert_type, Alert.status == 'OPEN').all():
        alert.status = 'RESOLVED'

def recent_watering_count(db: Session, device_id: str, now):
    since = now - timedelta(hours=1)
    return db.query(WateringEvent).filter(WateringEvent.device_id == device_id, WateringEvent.timestamp >= since).count()

def evaluate_automation(db: Session, device: Device, reading: SensorReading):
    now = as_utc(reading.timestamp) or now_utc()
    device.last_seen = now
    # Stop an active virtual pump when its safety duration expires or moisture is sufficiently restored.
    if device.pump_on:
        started = as_utc(device.pump_started_at) or now
        elapsed = (now - started).total_seconds()
        if elapsed >= settings.watering_duration_seconds or reading.soil_moisture >= min(100, device.moisture_threshold + 8):
            device.pump_on = False
            device.pump_started_at = None
        return

    if not device.auto_watering_enabled:
        return

    if reading.soil_moisture < device.moisture_threshold:
        last_event = db.query(WateringEvent).filter(WateringEvent.device_id == device.device_id).order_by(WateringEvent.timestamp.desc()).first()
        cooldown_ok = not last_event or (now - as_utc(last_event.timestamp)).total_seconds() >= settings.watering_cooldown_seconds
        tank_ok = reading.water_tank_level >= 10
        rate_ok = recent_watering_count(db, device.device_id, now) < settings.max_watering_events_per_hour
        if cooldown_ok and tank_ok and rate_ok:
            device.pump_on = True
            device.pump_started_at = now
            db.add(WateringEvent(
                event_id=f'WTR-{uuid4().hex[:10].upper()}', device_id=device.device_id,
                trigger_type='AUTO', moisture_before=reading.soil_moisture,
                duration_seconds=settings.watering_duration_seconds, timestamp=now
            ))
            add_alert(db, device.device_id, 'LOW_SOIL_MOISTURE', 'WARNING', f'{device.plant_name} moisture dropped below {device.moisture_threshold:.0f}%. Automatic watering started.')
        elif not tank_ok:
            add_alert(db, device.device_id, 'LOW_WATER_TANK', 'CRITICAL', f'{device.plant_name} water tank is below 10%. Watering was blocked.')
    else:
        resolve_alert(db, device.device_id, 'LOW_SOIL_MOISTURE')
    if reading.temperature > 35:
        add_alert(db, device.device_id, 'HIGH_TEMPERATURE', 'WARNING', f'{device.plant_name} temperature exceeded 35°C.')
    else:
        resolve_alert(db, device.device_id, 'HIGH_TEMPERATURE')

def device_status(device: Device):
    if not device.last_seen:
        return 'OFFLINE'
    age = (now_utc() - as_utc(device.last_seen)).total_seconds()
    return 'OFFLINE' if age > settings.offline_after_seconds else 'ONLINE'
