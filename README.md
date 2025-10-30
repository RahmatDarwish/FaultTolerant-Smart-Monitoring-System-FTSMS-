# Assignment3_ES

# Fault-Tolerant Smart Monitoring System (FTSMS)

A **fault-tolerant embedded system** built on the **Raspberry Pi Pico** that monitors temperature and humidity using **two redundant DHT sensors** and controls both a **fan** and **status LEDs**.  
The system is designed to **detect**, **handle**, and **recover** from both hardware and software faults using redundancy, watchdog timers, and safe-state logic.

---

## 🧠 Project Overview

This project was developed as part of the **2DT303 – Reliability in Embedded Systems** course at Linnaeus University.  
The main goal is to **investigate fault-tolerance mechanisms** in embedded systems by designing a simple but robust control system that maintains reliable operation under various fault conditions.

### 🎯 Objectives
- Demonstrate **fault detection and recovery** in a microcontroller-based system.
- Identify and analyze possible **fault scenarios** using **FMEA**.
- Implement **fault-tolerance strategies** (redundancy, watchdog, safe states).
- Test and evaluate system behavior under both **normal and faulty** conditions.

---

## ⚙️ Hardware Components

| Component | Quantity | Purpose |
|------------|-----------|----------|
| Raspberry Pi Pico | 1 | Main microcontroller |
| DHT11 / DHT22 Temperature-Humidity Sensor | 2 | Redundant environmental sensing |
| 5V DC Fan | 1 | Actuator for temperature control |
| LED (Red, Yellow, Green) | 3 | System status indicators |
| NPN Transistor (2N2222 or BC547) | 1 | Fan driver switch |
| 1N4007 Diode | 1 | Flyback protection for fan motor |
| 220 Ω Resistors | 3 | LED current limiting |
| 10 kΩ Resistors | 2 | Pull-ups for DHT sensors |
| Breadboard + Jumper Wires | — | Prototyping connections |
| USB Cable | 1 | Power and serial interface |

---

## 🔌 Circuit Overview

### 🧩 Basic Connections
- **DHT Sensors:** connected to GPIO 2 and GPIO 3 with 10 kΩ pull-ups.  
- **Fan:** powered by 5 V, controlled through NPN transistor on GPIO 15, diode across fan terminals.  
- **LEDs:**  
  - Green → Normal operation (GPIO 10)  
  - Yellow → Degraded mode (one sensor failed) (GPIO 11)  
  - Red → Safe/fault mode (both sensors failed) (GPIO 12)

> **Optional:** Add an OLED display (SSD1306) on I²C pins (GP0 = SDA, GP1 = SCL) to show live data and fault codes.

---

## 🧩 Software Architecture

```text
src/
├── main.py                # Main control loop
├── services/
│   ├── sensor_bus.py      # Reads and validates redundant sensors
│   ├── voter.py           # Consensus logic (redundancy handling)
│   ├── actuator.py        # Controls fan and LEDs
│   ├── faults.py          # Fault counters and logging
│   └── wdt_guard.py       # Watchdog timer management
└── docs/
    ├── FMEA_table.md
    ├── system_diagram.png
    └── test_results.md
