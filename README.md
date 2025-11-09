# Fault-Tolerant Smart Monitoring System (FTSMS)

The Fault-Tolerant Smart Monitoring System (FTSMS) is a Raspberry Pi Pico W project designed to provide reliable environmental monitoring with built-in fault-tolerance features. It measures temperature and humidity using two DHT11 sensors and sends live data to a Mosquitto MQTT broker through Wi-Fi. A web dashboard displays the readings, device status, and fault conditions in real time.

---

## System Overview
- **Microcontroller:** Raspberry Pi Pico W
- **Sensors:** Two DHT11 temperature and humidity sensors
- **Indicators:** RGB LED and active-low buzzer
- **Input:** Push button for alarm acknowledgment
- **Software features:**
  - Sensor voting logic for data validation
  - Watchdog timer for automatic recovery after freezes
  - Redundant LED and buzzer outputs for clear alerts
  - MQTT communication for remote monitoring

---

## Folder Structure

```
FTSMS/
├── main.py
├── ftsms_dashboard.html
└── services/
    ├── wifi.py
    ├── mqtt_client.py
    ├── indicators.py
    ├── button_handler.py
    ├── sensor_bus.py
    ├── voter.py
    └── wdt_guard.py
```

---

## Status Indicators
- **Green (Normal):** Both sensors work correctly and readings are valid.
- **Yellow (Degraded):** One sensor has failed but the system continues with the other.
- **Red (Fault):** Both sensors have failed or no valid data is available.
- **Buzzer:** Sounds during degraded or fault states. The button or an ACK command silences it. If the LED fails, the buzzer still alerts the user; if the buzzer fails, the LED still shows the fault.

---

## Fault-Tolerance Mechanisms
- **Sensor redundancy:** Two DHT11 sensors with a voter function ensure continuous operation even if one sensor fails.
- **Indicator redundancy:** LED and buzzer work together to prevent silent faults.
- **Watchdog timer:** Detects and recovers from software freezes by resetting the Pico.
- **Automatic reconnection:** Restores Wi-Fi and MQTT links after a network outage.

---

## How It Works
1. The Pico connects to Wi-Fi and the MQTT broker at startup.
2. The system reads both DHT11 sensors and compares the results.
3. The voter selects valid data and determines the system state.
4. The LED and buzzer display the current status.
5. The Pico publishes temperature, humidity, and status to the MQTT broker every second.
6. The dashboard receives the data and allows the user to send commands such as **ACK**, **RESET**, or **TEST**.

---

## Testing Summary
The system was tested under several fault conditions:
- One sensor disconnected → degraded mode.
- Both sensors disconnected → fault mode.
- LED or buzzer disconnected → redundancy maintained.
- Forced code freeze → watchdog reset and recovery.
- MQTT broker stopped → auto-reconnection confirmed.

Each test confirmed that the FTSMS continued to function, alert the user, or recover automatically.

---

## Summary
The FTSMS demonstrates how redundancy, watchdog timers, and voting logic can improve the reliability of small embedded systems. It maintains continuous monitoring and communication even when hardware or software faults occur.
