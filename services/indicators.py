
from machine import Pin
import time

class Indicators:
    def __init__(self, pin_r, pin_g, pin_b, pin_buzzer, active_low_buzzer=True):
        self.r = Pin(pin_r, Pin.OUT, value=0)
        self.g = Pin(pin_g, Pin.OUT, value=0)
        self.b = Pin(pin_b, Pin.OUT, value=0)
        self.buzzer = Pin(pin_buzzer, Pin.OUT, value=1 if active_low_buzzer else 0)
        self.active_low = active_low_buzzer
        self._buzz_on = False

    # Helpers
    def _led(self, r, g, b):
        """Turn LEDs on/off by color components."""
        self.r.value(1 if r else 0)
        self.g.value(1 if g else 0)
        self.b.value(1 if b else 0)

    def _buzz(self, on: bool):
        """Control buzzer state."""
        self._buzz_on = bool(on)
        if self.active_low:
            self.buzzer.value(0 if on else 1)
        else:
            self.buzzer.value(1 if on else 0)

    def is_buzzer_active_int(self):
        return 1 if self._buzz_on else 0

    # States
    def set_normal(self):
        """Green ON, buzzer off."""
        self._led(1, 0, 0)
        self._buzz(False)

    def set_degraded_pattern(self, silent=False):
        """Yellow (R+G), slow beep every 2s."""
        self._led(1, 1, 0)   
        if not silent:
            self._buzz(True)
            time.sleep(0.2)
            self._buzz(False)

    def set_fault_pattern(self, silent=False):
        """Flashing Red with fast beeps."""
        for _ in range(2):
            self._led(0, 1, 0) 
            if not silent:
                self._buzz(True)
            time.sleep(0.15)
            self._led(0, 0, 0) 
            if not silent:
                self._buzz(False)
            time.sleep(0.15)
        
        self._led(0, 1, 0)

    def test_blink(self):
        """Cycle through RGB colors for quick check."""
        for c in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]:
            self._led(*c)
            time.sleep(0.2)
        self._buzz(True)
        time.sleep(0.1)
        self._buzz(False)
        self.set_normal()
