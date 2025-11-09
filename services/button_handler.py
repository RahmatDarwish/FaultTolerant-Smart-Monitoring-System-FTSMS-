
from machine import Pin
import time

class Button:
    def __init__(self, pin, pull="up", debounce_ms=60):
        pull_const = Pin.PULL_UP if pull == "up" else Pin.PULL_DOWN
        self.btn = Pin(pin, Pin.IN, pull=pull_const)
        self.db_ms = debounce_ms
        self._last = time.ticks_ms()
        self._state = self._raw()

    def _raw(self):
        return 0 if self.btn.value() == 1 else 1 if self.btn.value() == 0 else 0

    def pressed(self):
        # Active when pulled to GND (with pull-up)
        now = time.ticks_ms()
        raw = 1 if self.btn.value() == 0 else 0
        if raw != self._state and time.ticks_diff(now, self._last) > self.db_ms:
            self._state = raw
            self._last = now
            if raw == 1:
                return True
        return False
