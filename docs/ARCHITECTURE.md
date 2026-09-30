# Architecture

```text
Virtual Python Sensor / ESP32
          |
       HTTPS
          v
     FastAPI REST API
          |
    +-----+----------+
    |                |
    v                v
PostgreSQL/SQLite  Automation Engine
    |                |
    v                v
History + Events  Virtual Pump / Relay command
    |                |
    +-------+--------+
            v
       React Dashboard
            |
          User
```

## Cloud mapping

- **SaaS:** the dashboard is consumed as an application rather than installed as a distributed enterprise system.
- **PaaS:** FastAPI and React can be deployed on managed application platforms.
- **IaaS:** a VM/container host can run the same Docker images.
- **Serverless:** the ingestion and automation service can be moved to cloud functions without changing the data contract.
- **API Gateway:** place an API gateway in front of the REST service for routing, throttling and authentication.
- **IoT broker:** MQTT can replace direct HTTPS for high-device-volume deployments.
- **Time-series storage:** sensor readings can move from PostgreSQL to a managed time-series store at scale.
- **Event-driven design:** a sensor event can trigger a function, automation decision, database write and notification.
