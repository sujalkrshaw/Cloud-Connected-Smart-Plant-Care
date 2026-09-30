# Cloud-Connected Smart Plant Care & Watering System — Project Report

## Abstract
This project implements a hardware-independent IoT cloud platform for monitoring plant conditions and automating irrigation. A Python simulator represents an IoT device and generates realistic environmental telemetry. A FastAPI service validates and stores telemetry, applies watering automation, tracks watering events, and creates alerts. A React dashboard provides near-real-time visibility, historical trends, analytics, alerts, threshold configuration, and manual watering. PostgreSQL is used in the Docker cloud-style deployment, while SQLite provides a lightweight local mode.

## Introduction
Manual watering is inconsistent and makes remote monitoring difficult. The proposed system combines sensor telemetry, cloud APIs, persistent storage, automation, and a web dashboard into one end-to-end workflow.

## Problem Statement
Plants can suffer from over-watering or under-watering when irrigation decisions are based only on manual observation. The system aims to make watering data-driven and remotely observable.

## Objectives
- Collect environmental telemetry.
- Store historical readings.
- Detect low moisture.
- Automate bounded watering.
- Generate alerts.
- Detect device offline conditions.
- Provide analytics and remote control.
- Demonstrate cloud-ready architecture without physical hardware.

## Existing System
A manual system depends on periodic human inspection and does not naturally provide historical analytics or remote control.

## Proposed System
The proposed architecture connects a virtual or physical IoT node to a REST API, database, automation engine, and dashboard.

## Industry Relevance
The same architectural pattern is applicable to smart agriculture, greenhouses, nurseries, vertical farming, landscaping, environmental monitoring, and smart-home automation.

## Cloud Computing Concepts
The project demonstrates managed-database thinking, REST APIs, serverless migration paths, event-driven automation, authentication, secrets, logging, monitoring, scalability, and deployment. The Docker configuration demonstrates a multi-service cloud-style environment.

## IoT Concepts
Telemetry, device identity, heartbeat/offline detection, actuator commands, sensor validation, retry behavior, and MQTT migration are demonstrated.

## Technology Stack
Python, FastAPI, SQLAlchemy, SQLite/PostgreSQL, React, Vite, Docker, REST, Pydantic, pytest.

## Architecture
Virtual sensor/ESP32 -> HTTPS/MQTT -> API layer -> database + automation -> pump command -> dashboard + alerts.

## Sensor Simulation
The simulator models moisture drying, moisture recovery while the virtual pump is active, gradual temperature/humidity changes, and a daylight curve.

## Database Design
Users, devices, sensor readings, watering events, and alerts are represented as relational tables with indexes for device/time and device/status queries.

## REST API
The service exposes telemetry ingestion, device management, latest/history, thresholds, manual watering, watering history, alerts, acknowledgement, and analytics endpoints.

## Watering Algorithm
Watering begins when moisture is below the configured threshold and safety checks pass. Cooldown, tank level, event-rate limits, and maximum duration prevent unsafe repeated activation.

## Dashboard
The React dashboard displays current telemetry, plant health, pump state, trends, analytics, alerts, watering history, and remote controls.

## Alerts
Low moisture, high temperature, low water tank, and offline conditions are represented as persistent alert records.

## Device Monitoring
The backend records `last_seen` on telemetry ingestion. A device becomes offline when the elapsed time exceeds the configured interval.

## Cloud Deployment
The Docker stack uses PostgreSQL, FastAPI, React/Nginx, and the simulator as separate services. The same logical services can be mapped to AWS, Azure, or GCP managed services.

## Testing
Automated tests cover health, validation, authentication, ingestion, automation, duplicates, thresholds, and history. Manual tests cover full simulation and failure modes.

## Security
The project uses API-key protected writes, input validation, environment-based configuration, bounded actuator commands, and explicit production security guidance.

## Scalability
At higher scale, device traffic can move to an IoT broker; processing can become serverless and asynchronous; storage can use managed time-series systems; queues, caching, aggregation, and retention can reduce load.

## Analytics
Average/minimum/maximum moisture, average temperature/humidity, and watering-event counts are calculated from stored data.

## Results
The system provides an end-to-end demonstration in which moisture gradually decreases, the backend starts a virtual pump below threshold, moisture recovers, and the dashboard records the event.

## Advantages
Hardware-independent demonstration, modular architecture, persistent history, automation, dashboard visibility, and clear migration path to physical ESP32 hardware.

## Limitations
The local project uses a demo API key and does not implement production-grade user identity, per-device certificates, real push notifications, or physical pump safety interlocks.

## Future Scope
MQTT, per-device certificates, Firebase/Supabase Auth, push/email notifications, ML-based irrigation prediction, weather integration, real water-consumption metering, multi-tenant authorization, and managed time-series storage.

## Conclusion
The project demonstrates how embedded/IoT telemetry can be transformed into a cloud-oriented application with storage, automation, monitoring, security, analytics, and deployment considerations.
