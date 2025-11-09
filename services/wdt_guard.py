
from machine import WDT

class WDTGuard:
    def __init__(self, timeout_ms=8000):
        self.wdt = None
        try:
            self.wdt = WDT(timeout=timeout_ms)
        except Exception:
            self.wdt = None

    def feed(self):
        if self.wdt:
            try:
                self.wdt.feed()
            except Exception:
                pass
