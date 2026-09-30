import os

API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000')
API_KEY = os.getenv('API_KEY', 'dev-plant-api-key')
DEVICE_ID = os.getenv('DEVICE_ID', 'PLANT-001')
INTERVAL_SECONDS = float(os.getenv('INTERVAL_SECONDS', '3'))
OFFLINE_MODE = os.getenv('OFFLINE_MODE', 'false').lower() == 'true'
START_MOISTURE = float(os.getenv('START_MOISTURE', '55'))
