def _avg(a, b):
    return (a + b) / 2.0

class Voter:
    def __init__(self, temp_tol_c=2.0, hum_tol_pct=6.0):
        self.temp_tol = temp_tol_c
        self.hum_tol = hum_tol_pct

    def fuse_state(self, ch1, ch2):
        # ch = (t, h, ok)
        t1, h1, ok1 = ch1
        t2, h2, ok2 = ch2

        if ok1 and ok2:
            # Compare deltas
            dt = abs(t1 - t2)
            dh = abs(h1 - h2)
            if dt <= self.temp_tol and dh <= self.hum_tol:
                fused_t = _avg(t1, t2)
                fused_h = _avg(h1, h2)
                return (fused_t, fused_h), "normal"
            else:
                # mismatch -> degraded; still provide fused mean
                fused_t = _avg(t1, t2)
                fused_h = _avg(h1, h2)
                return (fused_t, fused_h), "degraded"
        elif ok1 and not ok2:
            return (t1, h1), "degraded"
        elif ok2 and not ok1:
            return (t2, h2), "degraded"
        else:
            return None, "fault"
