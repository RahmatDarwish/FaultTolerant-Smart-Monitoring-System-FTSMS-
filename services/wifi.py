import time
import network

SSID = "<iotlab>"
PASSWORD = "<modermodemet>"

STATIC_IP = None

_wlan = network.WLAN(network.STA_IF)
_wlan.active(True)

def _apply_static():
    if STATIC_IP:
        ip, mask, gw, dns = STATIC_IP
        _wlan.ifconfig((ip, mask, gw, dns))

def connect(timeout_s: int = 15) -> bool:
    """Attempt a single connect with timeout. Returns True if connected."""
    if is_connected():
        return True
    _apply_static()
    try:
        _wlan.connect(SSID, PASSWORD)
    except Exception as e:
        return False

    t0 = time.ticks_ms()
    while not is_connected() and time.ticks_diff(time.ticks_ms(), t0) < timeout_s * 1000:
        time.sleep_ms(100)
    return is_connected()

def ensure_connected(max_retries: int = 10, backoff_start_s: int = 1, backoff_cap_s: int = 30) -> bool:
    """Connect with exponential backoff. Returns True if connected, else False."""
    if is_connected():
        return True
    attempt = 0
    delay = backoff_start_s
    while attempt < max_retries and not is_connected():
        attempt += 1
        ok = connect(timeout_s=15)
        if ok:
            return True
        time.sleep(delay)
        delay = min(delay * 2, backoff_cap_s)
    return is_connected()

def is_connected() -> bool:

    if not _wlan.active():
        return False
    st = _wlan.status()
    if st != network.STAT_GOT_IP and st != 3:
        return False
    ip = _wlan.ifconfig()[0]
    return ip is not None and ip != "0.0.0.0"

def ifconfig():
    return _wlan.ifconfig()

def disconnect():
    try:
        _wlan.disconnect()
    except Exception:
        pass
