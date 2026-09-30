import os
try:
    os.remove('./test_plant_care.db')
except FileNotFoundError:
    pass
os.environ['DATABASE_URL'] = 'sqlite:///./test_plant_care.db'
os.environ['API_KEY'] = 'test-key'
from fastapi.testclient import TestClient
from app.main import app
import pytest

HEADERS = {'X-API-Key': 'test-key'}
@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

def test_health(client):
    r = client.get('/health'); assert r.status_code == 200; assert r.json()['status'] == 'ok'

def test_invalid_sensor_rejected(client):
    r = client.post('/api/sensors/data', headers=HEADERS, json={'device_id':'PLANT-001','soil_moisture':120,'temperature':25,'humidity':50})
    assert r.status_code == 422

def test_sensor_and_automation(client):
    r = client.post('/api/sensors/data', headers=HEADERS, json={'reading_id':'TEST-001','device_id':'PLANT-001','soil_moisture':25,'temperature':28,'humidity':60,'light_level':50,'water_tank_level':100})
    assert r.status_code == 200
    assert r.json()['pump_on'] is True

def test_duplicate_sensor_is_idempotent(client):
    payload={'reading_id':'DUP-001','device_id':'PLANT-001','soil_moisture':50,'temperature':28,'humidity':60}
    a=client.post('/api/sensors/data',headers=HEADERS,json=payload)
    b=client.post('/api/sensors/data',headers=HEADERS,json=payload)
    assert a.status_code == 200 and b.status_code == 200
    assert b.json()['status'] == 'duplicate'

def test_threshold_update_and_history(client):
    r=client.put('/api/devices/PLANT-001/threshold',headers=HEADERS,json={'moisture_threshold':35})
    assert r.status_code == 200 and r.json()['moisture_threshold'] == 35
    r=client.get('/api/devices/PLANT-001/history'); assert r.status_code == 200

def test_manual_water_requires_auth(client):
    r=client.post('/api/devices/PLANT-001/water',json={'duration_seconds':3})
    assert r.status_code == 401
