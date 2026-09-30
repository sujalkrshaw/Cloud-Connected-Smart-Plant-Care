/* Optional physical-node example.
   Replace the placeholders with calibrated sensor libraries/pins for your board.
   The production system should use HTTPS and a device-specific credential.
*/
#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* API_URL = "https://YOUR_BACKEND.example.com/api/sensors/data";
const char* API_KEY = "YOUR_DEVICE_CREDENTIAL";
const int SOIL_PIN = 34;
const int PUMP_PIN = 26;

float soilPercent() {
  int raw = analogRead(SOIL_PIN);
  // Calibrate these two values for the actual sensor and soil.
  const int DRY = 3200;
  const int WET = 1200;
  float pct = 100.0f * (DRY - raw) / float(DRY - WET);
  return constrain(pct, 0, 100);
}

void setup() {
  Serial.begin(115200);
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float soil = soilPercent();
    String body = String("{\"device_id\":\"PLANT-001\",\"soil_moisture\":") + String(soil,1) +
                  ",\"temperature\":25,\"humidity\":60,\"light_level\":50,\"water_tank_level\":100}";
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-API-Key", API_KEY);
    int code = http.POST(body);
    // A production firmware should parse the response command and implement
    // a bounded local pump timer/failsafe rather than trusting an unbounded command.
    if (code > 0) Serial.printf("API response: %d\n", code);
    http.end();
  }
  delay(5000);
}
