from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String(80), default='demo-user', index=True)
    plant_name: Mapped[str] = mapped_column(String(120), default='Tomato Plant')
    plant_type: Mapped[str] = mapped_column(String(80), default='tomato')
    location: Mapped[str] = mapped_column(String(120), default='Indoor Garden')
    moisture_threshold: Mapped[float] = mapped_column(Float, default=40.0)
    pump_on: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_watering_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    pump_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class SensorReading(Base):
    __tablename__ = 'sensor_readings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reading_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), ForeignKey('devices.device_id'), index=True)
    soil_moisture: Mapped[float] = mapped_column(Float)
    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    light_level: Mapped[float] = mapped_column(Float, default=0.0)
    water_tank_level: Mapped[float] = mapped_column(Float, default=100.0)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

class WateringEvent(Base):
    __tablename__ = 'watering_events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), ForeignKey('devices.device_id'), index=True)
    trigger_type: Mapped[str] = mapped_column(String(40))
    moisture_before: Mapped[float] = mapped_column(Float)
    moisture_after: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alert_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), ForeignKey('devices.device_id'), index=True)
    alert_type: Mapped[str] = mapped_column(String(60))
    level: Mapped[str] = mapped_column(String(20), default='WARNING')
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default='OPEN', index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

Index('ix_sensor_device_time', SensorReading.device_id, SensorReading.timestamp)
Index('ix_event_device_time', WateringEvent.device_id, WateringEvent.timestamp)
Index('ix_alert_device_status', Alert.device_id, Alert.status)
