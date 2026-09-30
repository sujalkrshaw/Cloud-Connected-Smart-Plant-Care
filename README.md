# 🌱 Cloud-Connected Smart Plant Care & Watering System

> A hardware-independent IoT cloud platform for plant monitoring, automated irrigation, alerts, historical analytics, and remote control.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Vite-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## Overview

This project demonstrates an end-to-end **Cloud Computing + IoT** workflow without requiring physical hardware. A Python simulator behaves like an ESP32 sensor node, sends telemetry to a FastAPI backend, stores data in SQLite or PostgreSQL, evaluates watering rules, records alerts/events, and exposes a React dashboard for monitoring and control.

The simulator can later be replaced by an ESP32 with a capacitive soil-moisture sensor, DHT22/SHT31, and low-voltage pump driver while keeping the cloud API contract largely unchanged.

## Problem Statement

Manual watering is inconsistent. Plants can be over-watered or under-watered, while the owner has limited visibility when away. The system uses sensor telemetry and cloud automation to make watering decisions measurable, traceable, and remotely observable.

## Objectives

- Simulate IoT telemetry realistically.
- Store historical sensor data.
- Monitor plant health remotely.
- Automate irrigation below configurable thresholds.
- Prevent repeated or unsafe watering.
- Generate actionable alerts.
- Detect device offline conditions.
- Demonstrate cloud-ready architecture and deployment.
- Provide GitHub-quality proof of implementation and testing.

## Features

- 🌡️ Temperature/humidity monitoring
- 💧 Soil moisture monitoring
- ☀️ Simulated light level
- 🪣 Water-tank simulation
- 🤖 Automatic watering engine
- 🖱️ Manual cloud watering command
- 📈 Historical trend charts
- 🚨 Persistent alerts
- 📡 Device online/offline monitoring
- 🔐 API-key protected write/control endpoints
- 🧪 Automated backend tests
- 🐳 Docker Compose with PostgreSQL
- ☁️ Cloud migration architecture for AWS/Azure/GCP
- 🔌 Optional ESP32 hardware path

## Industry Relevance

The architecture maps to smart agriculture, precision farming, greenhouses, nurseries, vertical farming, hydroponics, smart homes, commercial landscaping, and environmental monitoring.

## Cloud Computing Concepts

| Concept | Where it appears |
|---|---|
| Cloud/remote monitoring | React dashboard + REST backend |
| IoT-to-cloud | Simulator/ESP32 -> HTTPS API |
| SaaS | Dashboard consumed as an application |
| PaaS | FastAPI/React can be hosted on managed application platforms |
| IaaS | Docker images can run on a VM |
| Cloud database | PostgreSQL container now; managed PostgreSQL in production |
| REST API | FastAPI endpoints |
| MQTT | Documented migration path for device fleets |
| Serverless | AWS Lambda/Azure Functions/GCP Cloud Run mapping |
| Event-driven architecture | Telemetry triggers automation and alerts |
| Scalability | Broker + API gateway + serverless + managed DB design |
| Authentication/authorization | API key now; production identity recommended |
| Secrets | Environment variables |
| Monitoring | Health endpoint + application logs |
| CI/CD | Docker/build/test workflow can be added to GitHub Actions |

## Architecture

```text
                    ┌─────────────────────┐
                    │ Virtual IoT Sensor  │
                    │ Python / ESP32      │
                    └──────────┬──────────┘
                               │ HTTPS / MQTT
                               ▼
                    ┌─────────────────────┐
                    │ FastAPI REST Layer  │
                    │ Validation + Auth   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       ┌────────────────┐           ┌──────────────────┐
       │ SQLite/Postgres│           │ Automation Engine│
       │ Sensor History │           │ Watering + Alerts│
       └───────┬────────┘           └─────────┬────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ React Dashboard     │
                    │ Charts + Controls   │
                    └──────────┬──────────┘
                               ▼
                             User
```

## Technology Stack

- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy
- **Database:** SQLite for simplest local mode; PostgreSQL for Docker/cloud-style mode
- **Frontend:** React + Vite + JavaScript
- **Simulation:** Python standard library
- **Deployment:** Docker Compose; cloud migration documented
- **Testing:** pytest + FastAPI TestClient

## Sensor Data Model

```json
{
  "reading_id": "RD-demo",
  "device_id": "PLANT-001",
  "soil_moisture": 32,
  "temperature": 29.4,
  "humidity": 61,
  "light_level": 72,
  "water_tank_level": 95,
  "timestamp": "2026-09-30T12:00:00+00:00"
}
```

## Database Design

### USERS
`user_id`, `name`, `email`, `created_at`

### DEVICES
`device_id`, `user_id`, `plant_name`, `plant_type`, `location`, `moisture_threshold`, `pump_on`, `last_seen`

### SENSOR_READINGS
`reading_id`, `device_id`, `soil_moisture`, `temperature`, `humidity`, `light_level`, `water_tank_level`, `timestamp`

### WATERING_EVENTS
`event_id`, `device_id`, `trigger_type`, `moisture_before`, `moisture_after`, `duration_seconds`, `timestamp`

### ALERTS
`alert_id`, `device_id`, `alert_type`, `level`, `message`, `status`, `created_at`, `acknowledged_at`

Indexes are included for device/time, event/time, and device/status queries.

## Automated Watering

For the default tomato profile:

```text
IF moisture < threshold
AND tank >= 10%
AND cooldown expired
AND hourly event limit not exceeded
THEN start virtual pump
```

The pump stops when moisture recovers above the target band or the maximum watering duration is reached.

## Plant Profiles

| Plant | Default threshold |
|---|---:|
| Succulent | 20% |
| Tomato | 40% |
| Herb | 35% |
| Indoor plant | 30% |

These are configurable demo values, not horticultural prescriptions. Real plants should use sensor calibration and species-specific agronomic guidance.

## REST API

See [`docs/API.md`](docs/API.md). Interactive Swagger documentation is available at `/docs` when the backend is running.

## Project Structure

```text
Cloud-Connected-Smart-Plant-Care/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── sensor_simulator/
│   ├── simulator.py
│   ├── config.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docs/
├── reports/
├── screenshots/
├── sample_data/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Local Installation — Windows PowerShell

### Prerequisites

- Python 3.11+ (3.13 recommended)
- Node.js 20+
- npm
- Git
- Docker Desktop (optional but recommended)

### Method A — simplest local SQLite mode

Terminal 1:

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care\frontend"
npm install
npm run dev
```

Terminal 3:

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care\sensor_simulator"
python simulator.py
```

Open `http://localhost:5173`.

### Method B — recommended Docker/PostgreSQL mode

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care"
docker compose up --build
```

Open `http://localhost:8080`.

API: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

Stop:

```powershell
docker compose down
```

## Virtual Simulation Walkthrough

1. Simulator starts around 55% moisture.
2. Moisture gradually falls toward the 40% threshold.
3. When the backend receives a dry reading, automation starts the virtual pump.
4. The simulator sees `pump_on=true` and increases moisture.
5. Once moisture recovers or the safety timer expires, the pump turns off.
6. A watering event is stored.
7. The dashboard displays the trend, alert, and event history.

## Testing

```powershell
cd backend
pytest -q
```

The automated suite covers API health, validation, authentication, sensor ingestion, watering automation, duplicate readings, threshold updates, and history.

## Security

The repository contains only a demo API key. Production deployment should use secret management, HTTPS, per-device identity, user authentication, authorization, rate limiting, key rotation, secure firmware, and database permissions. Never commit production credentials.

## Failure Handling

- **API failure:** simulator logs the failure and retries next cycle.
- **Duplicate reading:** backend returns `status=duplicate`.
- **Invalid values:** Pydantic returns HTTP 422.
- **Missing device:** HTTP 404.
- **Unauthorized writes:** HTTP 401.
- **Device offline:** dashboard status becomes OFFLINE after the configured timeout.
- **Low tank:** automatic watering is blocked and a critical alert is created.

## Scalability

For 10 devices, the current architecture is sufficient. For thousands of devices, use an IoT broker, API gateway, asynchronous processing, managed database, queues/event streams, aggregation, caching, and retention policies. For millions of readings, move telemetry to a managed time-series or analytical store and retain raw data according to business requirements.

## Cloud Deployment

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) and [`docs/AWS_ARCHITECTURE.md`](docs/AWS_ARCHITECTURE.md). The project intentionally distinguishes between a **local/cloud-style implementation** and a true managed production cloud deployment.

## Optional Hardware

See [`docs/HARDWARE.md`](docs/HARDWARE.md). The cloud API remains the same; the ESP32 replaces the Python simulator.

## Screenshot Evidence

See [`docs/SCREENSHOT_CHECKLIST.md`](docs/SCREENSHOT_CHECKLIST.md).

## Project Report

See [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md).

## Interview Preparation

See [`docs/INTERVIEW.md`](docs/INTERVIEW.md).

## GitHub Strategy

Repository name: **Cloud-Connected-Smart-Plant-Care**

Suggested topics:

`cloud-computing` `iot` `smart-agriculture` `python` `fastapi` `react` `postgresql` `rest-api` `automation` `smart-irrigation` `sensor-data` `cloud-monitoring` `docker`

Suggested commit history:

```text
Initialize smart plant cloud project
Add virtual IoT sensor simulator
Implement sensor REST API
Integrate cloud database
Add automated watering engine
Implement plant-specific thresholds
Add watering event tracking
Build real-time monitoring dashboard
Implement alert system
Add device offline detection
Add historical analytics
Add automated tests
Deploy application to cloud
Complete README and documentation
```

## Git Commands

```powershell
git init
git branch -M main
git add .
git commit -m "Initialize smart plant cloud project"
git remote add origin https://github.com/YOUR_USERNAME/Cloud-Connected-Smart-Plant-Care.git
git push -u origin main
```

If you want the staged development history, create commits after each milestone rather than one giant commit.

## Career Proof

See [`docs/CAREER_PROOF.md`](docs/CAREER_PROOF.md) for resume bullets, LinkedIn copy, technical skills, and the repository description.

## Limitations

This is an educational, hardware-free implementation. The default API key is intentionally a development credential. Production use requires stronger identity, authorization, TLS, device certificates/credentials, physical safety interlocks, real notification providers, and calibrated sensors.

## Future Improvements

- MQTT + managed IoT broker
- Firebase/Supabase/Auth integration
- Push/email notifications
- Weather-aware irrigation
- ML-based watering prediction
- ESP32 secure firmware
- Per-device certificates
- Multi-tenant RBAC
- Managed time-series analytics
- Water-flow meter integration

## Learning Outcomes

This project demonstrates practical understanding of **Cloud Computing, IoT-to-cloud communication, REST APIs, databases, automation, authentication, Docker, testing, monitoring, scalability, and full-stack development**.

## Author

**Sujal Shaw**  
B.Tech Electronics & Communication Engineering  
Cloud Computing · IoT · Python · Full-Stack Development
