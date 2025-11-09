import time
try:
    import dht
    from machine import Pin
except Exception as e:
    dht = None
    Pin = None

class SensorBus:
    def __init__(self, pin_dht1, pin_dht2):
        """Initialize both DHT11 sensors on given GPIO pins."""
        self.pin1 = Pin(pin_dht1) if Pin else None
        self.pin2 = Pin(pin_dht2) if Pin else None

        self.s1 = dht.DHT11(self.pin1) if dht and self.pin1 else None
        self.s2 = dht.DHT11(self.pin2) if dht and self.pin2 else None

        # DHT11 requires at least 1 second between readings
        self._min_interval_ms = 1000
        self._last_ms = 0

    def _read_one(self, sensor):
        """Try to read one DHT11; return (t, h, ok)."""
        if not sensor:
            return None, None, False
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()

            if t is None or h is None:
                return None, None, False
            # sanity check
            if not (0 <= t <= 50 and 10 <= h <= 90):
                return None, None, False

            return float(t), float(h), True
        except Exception:
            return None, None, False

    def read_pair(self):
        """Read both DHT11 sensors, return (t1,h1,ok1,t2,h2,ok2)."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_ms) < self._min_interval_ms:
            # too soon since last read, wait a bit
            time.sleep_ms(self._min_interval_ms)
        self._last_ms = time.ticks_ms()

        t1, h1, ok1 = self._read_one(self.s1)
        time.sleep_ms(50)  
        t2, h2, ok2 = self._read_one(self.s2)
        return t1, h1, ok1, t2, h2, ok2
