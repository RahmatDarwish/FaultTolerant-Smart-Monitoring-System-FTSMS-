from machine import Pin
import dht
import time

sensor1 = dht.DHT11(Pin(17))
sensor2 = dht.DHT11(Pin(16))

print("Starting DHT11 dual-sensor test...\n")

while True:
    try:
        # Read sensor 1
        sensor1.measure()
        t1 = sensor1.temperature()
        h1 = sensor1.humidity()

        # Read sensor 2
        sensor2.measure()
        t2 = sensor2.temperature()
        h2 = sensor2.humidity()

        # Display both sensor readings
        print(f"Sensor1 -> Temp: {t1}°C | Humidity: {h1}%")
        print(f"Sensor2 -> Temp: {t2}°C | Humidity: {h2}%")

        # Check if readings differ significantly (basic comparison)
        if abs(t1 - t2) > 2 or abs(h1 - h2) > 5:
            print("⚠️ Warning: Sensors readings differ more than expected!\n")
        else:
            print("✅ Both sensors are reading normally.\n")

    except Exception as e:
        print("Error reading sensors:", e)

    time.sleep(2)
