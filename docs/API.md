# REST API

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/health` | Service health | No |
| GET | `/api/devices` | List devices | No |
| POST | `/api/devices` | Register device | API key |
| GET | `/api/devices/{id}` | Device metadata/status | No |
| POST | `/api/sensors/data` | Ingest reading | API key |
| GET | `/api/devices/{id}/latest` | Latest reading | No |
| GET | `/api/devices/{id}/history` | Historical readings | No |
| PUT | `/api/devices/{id}/threshold` | Change threshold | API key |
| PUT | `/api/devices/{id}/automation` | Enable/disable automatic watering | API key |
| POST | `/api/devices/{id}/water` | Manual watering | API key |
| GET | `/api/devices/{id}/watering-history` | Watering events | No |
| GET | `/api/alerts` | Alerts | No |
| PUT | `/api/alerts/{id}/acknowledge` | Acknowledge alert | API key |
| GET | `/api/analytics/{id}` | Aggregate analytics | No |

Sensor data is validated using Pydantic. Invalid ranges return HTTP 422. Missing/incorrect API keys return HTTP 401. Missing devices return HTTP 404. Duplicate reading IDs return HTTP 200 with `status=duplicate` so retries remain idempotent.
