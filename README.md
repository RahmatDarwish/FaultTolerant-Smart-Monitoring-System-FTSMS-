# Fault-Tolerant Smart Monitoring System (FTSMS)

A **fault-tolerant embedded system** built on the **Raspberry Pi Pico W** that monitors temperature and humidity using **two redundant DHT sensors** and provides system feedback through an **RGB LED**, **buzzer**, and **push button**.  
The system is designed to **detect**, **handle**, and **recover** from both hardware and software faults using redundancy, watchdog timers, and safe-state logic.

---

## Project Overview

This project was developed as part of the **2DT303 – Reliability in Embedded Systems** course at **Linnaeus University**.  
The main objective is to **investigate fault-tolerance mechanisms** in embedded systems by designing a robust control system that maintains reliable operation under various fault conditions.

### Objectives
- Demonstrate **fault detection and recovery** in a microcontroller-based system.  
- Identify and analyze possible **fault scenarios** using **FMEA**.  
- Implement **fault-tolerance strategies** such as redundancy, watchdogs, and safe states.  
- Evaluate system behavior under both **normal** and **faulty** conditions.

---

## Hardware Components

| Component | Quantity | Purpose |
|------------|-----------|----------|
| **Raspberry Pi Pico W** | 1 | Main microcontroller (with Wi-Fi) |
| **DHT11 / DHT22 Sensors** | 2 | Redundant temperature-humidity sensors |
| **RGB LED Module (CNT1)** | 1 | Visual status indicator (Normal / Degraded / Fault) |
| **Active Buzzer** | 1 | Audible alarm for warnings or fault alerts |
| **Push Button** | 1 | Manual reset and user acknowledgment |
| **220 Ω Resistors** | 3 | LED current limiting for RGB channels |
| **10 kΩ Resistors** | 3 | Pull-ups for DHT sensors and button input |
| **Breadboard + Jumper Wires** | — | Prototyping and connections |
| **USB Cable** | 1 | Power and serial communication |

---

## Circuit Overview

### Basic Connections

- **DHT Sensors:** connected to GPIO 2 and GPIO 3 with 10 kΩ pull-ups.  
- **RGB LED (common-cathode):**  
  - Red → GPIO 12  
  - Green → GPIO 11  
  - Blue → GPIO 10  
  - Cathode (–) → GND  
- **Buzzer:** connected to GPIO 15.  
- **Push Button:** connected to GPIO 14 with a 10 kΩ pull-up to 3.3 V.  
- **All grounds are common** between the Pico, sensors, RGB LED, and buzzer.

> **Status Logic:**  
> **Normal** – Green LED ON, buzzer OFF  
> **Degraded** – Red + Green (Yellow) LED + slow buzzer beeps  
> **Fault** – Red LED flashing + fast buzzer alarm  
> **Acknowledged / Safe Mode** – Button press resets fault state and restarts normal operation

---

## Wi-Fi & Web Dashboard Extension

To enhance fault-tolerance study and demonstrate system communication, FTSMS includes a **Wi-Fi data logging and visualization module** using the **Raspberry Pi Pico W**.

### System Architecture

| Layer | Description |
|--------|-------------|
| **Core 0** | Handles real-time control: sensor readings, redundancy logic, RGB LED, buzzer, and button input. |
| **Core 1** | Manages Wi-Fi connectivity, data transmission, and server communication. |
| **Web Dashboard** | Displays temperature, humidity, and system status in real time. |

When a network or server fault occurs, data are **buffered locally** and automatically **transmitted** once connectivity is restored.

---

### Communication Workflow

1. **Sensor Sampling:** Both DHT sensors acquire temperature and humidity.  
2. **Fault Detection:** Data validated using redundancy voting logic.  
3. **System Feedback:** RGB LED and buzzer respond to current fault state.  
4. **User Control:** Button press resets or acknowledges faults.  
5. **Data Packaging:** Sensor data formatted as JSON and sent over Wi-Fi.

```json
{
  "device_id": "ftsms-pico-01",
  "seq": 215,
  "temperature_c": 23.7,
  "humidity_pct": 47.1,
  "status": "degraded",
  "buzzer": 1,
  "wifi_status": "ok"
}
```

---

## Software Architecture

```text
src/
├── main.py                # Main control loop
├── services/
│   ├── sensor_bus.py      # Reads redundant DHT sensors
│   ├── voter.py           # Fault voting and validation logic
│   ├── indicators.py      # RGB LED and buzzer control
│   ├── button_handler.py  # Manual reset and user input
│   ├── faults.py          # Fault logging and safe-state behavior
│   └── wdt_guard.py       # Watchdog timer for recovery
└── docs/
    ├── FMEA_table.md
    ├── system_diagram.png
    └── test_results.md
```

---

## 🧠 Safe-State & Recovery Logic

When both sensors fail, or when system communication errors persist:
- RGB LED → solid red  
- Buzzer → active continuous alarm  
- Button press → resets watchdog, clears fault flags, and attempts recovery

If the system cannot recover, it remains in a **safe (fault) state** until manual intervention.

---

## 🧪 Testing & Validation

| Test Case | Condition | Expected Behavior |
|------------|------------|-------------------|
| **Normal Operation** | Both DHT sensors active and consistent | Green LED ON, buzzer silent |
| **Degraded Mode** | One DHT sensor fails or data mismatch | Yellow LED, slow buzzer beeps |
| **Fault Mode** | Both sensors fail or watchdog timeout | Red LED flashing, fast buzzer beeps |
| **User Reset** | Button pressed during fault | System resets and returns to normal operation |
| **Wi-Fi Fault** | Network unavailable | Data buffered locally, re-sent once restored |

---

## 🧾 Summary

The FTSMS demonstrates **fault detection, isolation, and recovery** in an embedded control system using low-cost, widely available components.  
By replacing the motor actuator with an **RGB LED**, **buzzer**, and **button**, the system provides **clear multimodal feedback** on its reliability state while maintaining fault-tolerant design principles.
