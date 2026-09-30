"""Hardware-free virtual IoT node for the Smart Plant project."""
import json, logging, math, random, time, uuid
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from config import API_URL, API_KEY, DEVICE_ID, INTERVAL_SECONDS, OFFLINE_MODE, START_MOISTURE

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

class VirtualPlant:
    def __init__(self):
        self.moisture = START_MOISTURE
        self.temperature = 27.0
        self.humidity = 60.0
        self.light = 50.0
        self.tank = 100.0

    def evolve(self, pump_on: bool):
        if pump_on:
            self.moisture = min(100, self.moisture + random.uniform(2.5, 4.0))
            self.tank = max(0, self.tank - random.uniform(0.5, 1.2))
        else:
            self.moisture = max(0, self.moisture - random.uniform(0.8, 1.5))
        hour = (time.time() / 3600) % 24
        daylight = max(0, math.sin((hour - 6) / 12 * math.pi))
        self.light = max(0, min(100, daylight * 90 + random.uniform(-4, 4)))
        self.temperature += random.uniform(-0.35, 0.35)
        self.temperature += (28 - self.temperature) * 0.05
        self.humidity += random.uniform(-1.2, 1.2)
        self.humidity += (62 - self.humidity) * 0.05

    def payload(self):
        return {
            'reading_id': f'RD-{uuid.uuid4().hex}',
            'device_id': DEVICE_ID,
            'soil_moisture': round(self.moisture, 2),
            'temperature': round(self.temperature, 2),
            'humidity': round(max(0, min(100, self.humidity)), 2),
            'light_level': round(self.light, 2),
            'water_tank_level': round(self.tank, 2),
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }

def post(payload):
    if OFFLINE_MODE:
        logging.info('OFFLINE MODE | generated=%s', json.dumps(payload))
        return {'pump_on': False}
    body = json.dumps(payload).encode()
    req = Request(f'{API_URL}/api/sensors/data', data=body, method='POST', headers={'Content-Type':'application/json','X-API-Key':API_KEY})
    with urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode())

def main():
    plant = VirtualPlant()
    pump = False
    logging.info('Virtual IoT node started: %s | interval=%ss', DEVICE_ID, INTERVAL_SECONDS)
    while True:
        plant.evolve(pump)
        payload = plant.payload()
        try:
            result = post(payload)
            pump = bool(result.get('pump_on', False))
            logging.info('MOISTURE=%5.1f%% TEMP=%4.1fC HUM=%4.1f%% LIGHT=%4.1f%% TANK=%4.1f%% | CLOUD=%s PUMP=%s', plant.moisture, plant.temperature, plant.humidity, plant.light, plant.tank, result.get('status','offline'), 'ON' if pump else 'OFF')
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            logging.error('Cloud request failed: %s | retrying next cycle', exc)
        time.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    main()
