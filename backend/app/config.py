import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv('APP_NAME', 'Cloud-Connected Smart Plant Care API')
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./plant_care.db')
    api_key: str = os.getenv('API_KEY', 'dev-plant-api-key')
    cors_origins: str = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
    offline_after_seconds: int = int(os.getenv('OFFLINE_AFTER_SECONDS', '20'))
    watering_duration_seconds: int = int(os.getenv('WATERING_DURATION_SECONDS', '6'))
    watering_cooldown_seconds: int = int(os.getenv('WATERING_COOLDOWN_SECONDS', '30'))
    max_watering_events_per_hour: int = int(os.getenv('MAX_WATERING_EVENTS_PER_HOUR', '4'))

settings = Settings()
