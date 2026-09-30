# Optional ESP32 Hardware Version

## Components

- ESP32 development board
- Capacitive soil-moisture sensor
- DHT22 or SHT31 temperature/humidity sensor
- Low-voltage DC pump
- Relay module or logic-level MOSFET driver appropriate for the pump
- Separate 5–12 V supply sized for the pump
- Tubing and reservoir

## Conceptual wiring

- Soil sensor analog output -> ESP32 ADC input.
- DHT22 data -> ESP32 digital GPIO with the required pull-up.
- Pump driver control input -> ESP32 GPIO.
- Sensor and ESP32 grounds share a common low-voltage ground.
- Pump power comes from its suitable external supply through the driver.
- **Do not power a pump directly from an ESP32 GPIO.**
- Use a flyback diode where required by the chosen motor/driver circuit.

## Firmware flow

1. Connect to Wi-Fi.
2. Read sensors.
3. Validate values locally.
4. POST the same JSON contract used by `sensor_simulator/simulator.py`.
5. Read the API command response or use a secure MQTT command topic.
6. Drive the relay/MOSFET for a bounded duration.
7. Report the next reading.

The cloud architecture does not need to change: the only replacement is the virtual sensor node with the physical ESP32.
