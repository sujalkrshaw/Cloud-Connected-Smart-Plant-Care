# Enterprise Cloud Architecture

```text
ESP32 / Simulator
      |
 AWS IoT Core (MQTT)
      |
 API Gateway / IoT Rules
      |
 Lambda / EventBridge
   /        |         \
DynamoDB  Timestream   SNS
   |          |          |
   +----------+----------+
              |
        React Dashboard
              |
             S3

CloudWatch -> logs, metrics, alarms
```

## Azure equivalent

IoT Hub -> Functions -> Cosmos DB / Azure Data Explorer -> Service Bus / Notification Hubs -> Static Web Apps -> Application Insights.

## GCP equivalent

Pub/Sub / IoT-compatible gateway -> Cloud Run / Cloud Functions -> Firestore / BigQuery -> Cloud Tasks / notification provider -> Firebase Hosting -> Cloud Monitoring.

The local implementation intentionally keeps the same logical boundaries so a student can explain the migration path without pretending that local SQLite is itself a managed cloud database.
