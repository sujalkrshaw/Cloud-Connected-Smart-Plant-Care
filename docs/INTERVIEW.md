# Interview Preparation — 10 Questions & Answers

## 1. Explain your project.
I built a cloud-connected smart plant monitoring and watering platform. Because I did not depend on physical hardware, I created a Python virtual IoT node that generates realistic soil moisture, temperature, humidity, light, and water-tank readings. The node sends readings over HTTPS to a FastAPI backend. The backend validates and stores the data in SQLite locally or PostgreSQL in Docker, evaluates watering rules, creates alerts, and exposes REST APIs. A React dashboard polls the API for near-real-time monitoring, charts, analytics, alerts, threshold configuration, and manual watering. The architecture is designed so the simulator can later be replaced by an ESP32 without changing the cloud data contract.

## 2. How does data move from the sensor to the dashboard?
The simulator creates a timestamped JSON reading, authenticates with an API key, and posts it to `/api/sensors/data`. FastAPI validates it with Pydantic, writes it to the database, runs the automation engine, and returns the pump command. The React dashboard calls latest/history/analytics/alerts endpoints and updates the UI every three seconds.

## 3. Why did you use REST instead of MQTT?
REST is simple to demonstrate and easy to debug for a student cloud project. MQTT is a better fit for large fleets because it is lightweight and publish/subscribe based. My architecture keeps the device contract separate from the transport, so MQTT can be introduced through an IoT broker later.

## 4. How is the watering decision generated?
Each accepted reading is compared with the device's configurable moisture threshold. Watering starts only when moisture is below the threshold, the tank is above the minimum level, the cooldown has expired, and the hourly event limit has not been exceeded. A maximum duration and moisture recovery condition stop the pump.

## 5. How did you prevent repeated watering?
I used three controls: a cooldown window, a maximum number of watering events per hour, and an active-pump state with a bounded duration. This prevents a stream of low readings from continuously starting the pump.

## 6. How would you scale it to thousands of devices?
I would move device traffic to an MQTT broker or managed IoT service, place an API gateway or event rules layer in front of serverless processing, use a managed time-series or scalable database, and process bursts asynchronously through queues or event streams. The dashboard would query aggregated data rather than every raw event.

## 7. What security controls are present?
Write/control endpoints require an API key, request values are validated, duplicate readings are detected, and secrets are kept in environment variables rather than source code. For production I would replace the demo API key with per-device credentials and user authentication, use HTTPS everywhere, rotate secrets, apply rate limits, and enforce authorization per user/device.

## 8. What happens if the API goes down?
The simulator catches network errors, logs the failure, and continues its local simulation. It attempts the next cycle again. In a production device I would add exponential backoff and a local queue so readings are buffered until connectivity returns.

## 9. How did you test the system?
I created automated API tests for health, validation, authentication, sensor ingestion, automation, duplicate handling, threshold updates, and history. I also use manual end-to-end tests for simulator behavior, dashboard rendering, offline detection, and database failure scenarios.

## 10. How would you deploy it to AWS?
A production design could use AWS IoT Core for MQTT device connectivity, API Gateway and Lambda for APIs and automation, DynamoDB or Timestream for storage, SNS for notifications, S3 for static frontend hosting, and CloudWatch for logs and monitoring. The local FastAPI/PostgreSQL implementation demonstrates the same logical separation without requiring paid infrastructure.
