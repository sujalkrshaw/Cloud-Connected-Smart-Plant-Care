from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SensorData(BaseModel):
    reading_id: str | None = None
    device_id: str = Field(min_length=2, max_length=80)
    soil_moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-20, le=70)
    humidity: float = Field(ge=0, le=100)
    light_level: float = Field(default=0, ge=0, le=100)
    water_tank_level: float = Field(default=100, ge=0, le=100)
    timestamp: datetime | None = None

class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=2, max_length=80)
    plant_name: str = Field(default='Tomato Plant', min_length=1, max_length=120)
    plant_type: str = Field(default='tomato', min_length=1, max_length=80)
    location: str = Field(default='Indoor Garden', max_length=120)
    moisture_threshold: float = Field(default=40, ge=1, le=99)

class ThresholdUpdate(BaseModel):
    moisture_threshold: float = Field(ge=1, le=99)

class WaterRequest(BaseModel):
    duration_seconds: int = Field(default=5, ge=1, le=30)

class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    device_id: str
    user_id: str
    plant_name: str
    plant_type: str
    location: str
    moisture_threshold: float
    pump_on: bool
    auto_watering_enabled: bool
    last_seen: datetime | None
    created_at: datetime
