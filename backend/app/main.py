from datetime import datetime, timezone
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, Depends, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from .config import settings
from .database import Base, engine, get_db
from .models import User, Device, SensorReading, WateringEvent, Alert
from .schemas import SensorData, DeviceCreate, DeviceOut, ThresholdUpdate, WaterRequest
from pydantic import BaseModel, Field

class AutomationUpdate(BaseModel):
    enabled: bool
from .services import evaluate_automation, device_status, now_utc, PLANT_PROFILES

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app):
    db = next(get_db())
    try:
        ensure_demo_device(db)
        yield
    finally:
        db.close()

app = FastAPI(title=settings.app_name, version='1.0.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(',') if x.strip()], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')

def get_device_or_404(db, device_id):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    return device

def ensure_demo_device(db):
    device = db.query(Device).filter(Device.device_id == 'PLANT-001').first()
    if not device:
        db.add(User(user_id='demo-user', name='Demo User', email='demo@example.com'))
        device = Device(device_id='PLANT-001', plant_name='Tomato Plant', plant_type='tomato', location='Virtual Greenhouse', moisture_threshold=40)
        db.add(device); db.commit(); db.refresh(device)
    return device

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'smart-plant-api', 'timestamp': now_utc()}

@app.get('/api/plant-profiles')
def plant_profiles():
    return PLANT_PROFILES

@app.post('/api/devices', response_model=DeviceOut, dependencies=[Depends(require_api_key)])
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    if db.query(Device).filter(Device.device_id == payload.device_id).first():
        raise HTTPException(409, 'Device already exists')
    device = Device(**payload.model_dump())
    db.add(device); db.commit(); db.refresh(device)
    return device

@app.get('/api/devices', response_model=list[DeviceOut])
def devices(db: Session = Depends(get_db)):
    return db.query(Device).order_by(Device.created_at.asc()).all()

@app.get('/api/devices/{device_id}')
def device_detail(device_id: str, db: Session = Depends(get_db)):
    d = get_device_or_404(db, device_id)
    status = device_status(d)
    if status == 'OFFLINE' and d.last_seen:
        from .services import add_alert
        add_alert(db, d.device_id, 'DEVICE_OFFLINE', 'CRITICAL', f'No sensor data received from {d.device_id} during the expected interval.')
        db.commit()
    return {**DeviceOut.model_validate(d).model_dump(), 'status': status}

@app.post('/api/sensors/data', dependencies=[Depends(require_api_key)])
def ingest_sensor_data(payload: SensorData, db: Session = Depends(get_db)):
    d = get_device_or_404(db, payload.device_id)
    rid = payload.reading_id or f'RD-{uuid4().hex}'
    if db.query(SensorReading).filter(SensorReading.reading_id == rid).first():
        return {'status': 'duplicate', 'reading_id': rid, 'pump_on': d.pump_on}
    timestamp = payload.timestamp or now_utc()
    reading = SensorReading(reading_id=rid, timestamp=timestamp, **payload.model_dump(exclude={'reading_id','timestamp'}))
    db.add(reading)
    evaluate_automation(db, d, reading)
    db.commit()
    return {'status': 'accepted', 'reading_id': rid, 'pump_on': d.pump_on, 'device_status': device_status(d), 'moisture_threshold': d.moisture_threshold}

@app.get('/api/devices/{device_id}/latest')
def latest(device_id: str, db: Session = Depends(get_db)):
    d = get_device_or_404(db, device_id)
    if device_status(d) == 'OFFLINE' and d.last_seen:
        from .services import add_alert
        add_alert(db, d.device_id, 'DEVICE_OFFLINE', 'CRITICAL', f'No sensor data received from {d.device_id} during the expected interval.')
        db.commit()
    r = db.query(SensorReading).filter(SensorReading.device_id == device_id).order_by(SensorReading.timestamp.desc()).first()
    if not r: return {'device': DeviceOut.model_validate(d).model_dump(), 'reading': None, 'status': device_status(d)}
    return {'device': DeviceOut.model_validate(d).model_dump(), 'reading': r.__dict__ | {'_sa_instance_state': None}, 'status': device_status(d)}

@app.get('/api/devices/{device_id}/history')
def history(device_id: str, limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    get_device_or_404(db, device_id)
    rows = db.query(SensorReading).filter(SensorReading.device_id == device_id).order_by(SensorReading.timestamp.desc()).limit(limit).all()
    return list(reversed([{k:v for k,v in r.__dict__.items() if k != '_sa_instance_state'} for r in rows]))

@app.put('/api/devices/{device_id}/automation', dependencies=[Depends(require_api_key)])
def automation(device_id: str, payload: AutomationUpdate, db: Session = Depends(get_db)):
    d = get_device_or_404(db, device_id); d.auto_watering_enabled = payload.enabled; db.commit()
    return {'device_id': device_id, 'auto_watering_enabled': d.auto_watering_enabled}

@app.put('/api/devices/{device_id}/threshold', dependencies=[Depends(require_api_key)])
def threshold(device_id: str, payload: ThresholdUpdate, db: Session = Depends(get_db)):
    d = get_device_or_404(db, device_id); d.moisture_threshold = payload.moisture_threshold; db.commit()
    return {'device_id': device_id, 'moisture_threshold': d.moisture_threshold}

@app.post('/api/devices/{device_id}/water', dependencies=[Depends(require_api_key)])
def manual_water(device_id: str, payload: WaterRequest, db: Session = Depends(get_db)):
    d = get_device_or_404(db, device_id)
    if d.pump_on: raise HTTPException(409, 'Pump is already running')
    now = now_utc(); d.pump_on = True; d.pump_started_at = now
    latest_reading = db.query(SensorReading).filter(SensorReading.device_id == device_id).order_by(SensorReading.timestamp.desc()).first()
    before = latest_reading.soil_moisture if latest_reading else 0
    db.add(WateringEvent(event_id=f'WTR-{uuid4().hex[:10].upper()}', device_id=device_id, trigger_type='MANUAL', moisture_before=before, duration_seconds=payload.duration_seconds, timestamp=now))
    db.commit()
    return {'status':'started','pump_on':True,'duration_seconds':payload.duration_seconds}

@app.get('/api/devices/{device_id}/watering-history')
def watering_history(device_id: str, db: Session = Depends(get_db)):
    get_device_or_404(db, device_id)
    rows = db.query(WateringEvent).filter(WateringEvent.device_id == device_id).order_by(WateringEvent.timestamp.desc()).limit(100).all()
    return [{k:v for k,v in r.__dict__.items() if k != '_sa_instance_state'} for r in rows]

@app.get('/api/alerts')
def alerts(device_id: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Alert)
    if device_id: q = q.filter(Alert.device_id == device_id)
    rows = q.order_by(Alert.created_at.desc()).limit(100).all()
    return [{k:v for k,v in r.__dict__.items() if k != '_sa_instance_state'} for r in rows]

@app.put('/api/alerts/{alert_id}/acknowledge', dependencies=[Depends(require_api_key)])
def acknowledge(alert_id: str, db: Session = Depends(get_db)):
    a = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not a: raise HTTPException(404, 'Alert not found')
    a.status = 'ACKNOWLEDGED'; a.acknowledged_at = now_utc(); db.commit()
    return {'status':'acknowledged','alert_id':alert_id}

@app.get('/api/analytics/{device_id}')
def analytics(device_id: str, db: Session = Depends(get_db)):
    get_device_or_404(db, device_id)
    stats = db.query(
        func.avg(SensorReading.soil_moisture), func.min(SensorReading.soil_moisture), func.max(SensorReading.soil_moisture),
        func.avg(SensorReading.temperature), func.avg(SensorReading.humidity)
    ).filter(SensorReading.device_id == device_id).one()
    count = db.query(WateringEvent).filter(WateringEvent.device_id == device_id).count()
    return {'average_moisture': stats[0] or 0, 'min_moisture': stats[1] or 0, 'max_moisture': stats[2] or 0, 'average_temperature': stats[3] or 0, 'average_humidity': stats[4] or 0, 'watering_events': count}
