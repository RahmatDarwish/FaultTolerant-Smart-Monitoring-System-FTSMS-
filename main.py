
BROKER_IP = "192.168.1.10"  
WIFI_SSID = "iotlab"
WIFI_PASS = "modermodemet"

# Imports
import time
from machine import unique_id, Pin
import ubinascii

from services import wifi
from services.mqtt_client import MQTTClientWrapper, TOPIC_DATA, TOPIC_CMD
from services.indicators import Indicators
from services.button_handler import Button
from services.sensor_bus import SensorBus
from services.voter import Voter
from services.wdt_guard import WDTGuard

PIN_LED_R = 15
PIN_LED_G = 14
PIN_LED_B = 13

PIN_BUZZER = 12          
PIN_BUTTON = 11          

PIN_DHT1 = 16
PIN_DHT2 = 17

# Initialize hardware helpers 
ind = Indicators(PIN_LED_R, PIN_LED_G, PIN_LED_B, PIN_BUZZER, active_low_buzzer=True)
btn = Button(PIN_BUTTON, pull="up", debounce_ms=80)
bus = SensorBus(PIN_DHT1, PIN_DHT2)  
voter = Voter(temp_tol_c=2.0, hum_tol_pct=6.0)

# Wi-Fi + MQTT
wifi.SSID = WIFI_SSID
wifi.PASSWORD = WIFI_PASS
client_id = "ftsms-" + ubinascii.hexlify(unique_id()).decode()
mc = MQTTClientWrapper(client_id=client_id, broker=BROKER_IP, port=1883)

# Watchdog
wdt_guard = WDTGuard(timeout_ms=8000)

# State
seq = 0
acknowledged = False   
normal_streak = 0      
force_test = False

# Command handler
def on_cmd(topic, msg):
    global acknowledged, force_test
    t = topic.decode() if isinstance(topic, (bytes, bytearray)) else str(topic)
    m = msg.decode() if isinstance(msg, (bytes, bytearray)) else str(msg)
    if t == "ftsms/command":
        ml = m.lower()
        if ml == "reset":
            acknowledged = False
        elif ml == "ack":
            acknowledged = True
        elif ml == "test":
            force_test = True

# Publish helper
def publish(mc, payload: dict):
    mc.publish_json(TOPIC_DATA, payload)

# Main loop body
def loop():
    global seq, acknowledged, normal_streak, force_test

    # Connectivity
    wifi.ensure_connected()
    if not mc.is_connected():
        try:
            mc.set_callback(on_cmd)
            mc.connect_and_subscribe([(TOPIC_CMD, 0)])
        except Exception:
            ind.set_degraded_pattern()
            time.sleep(0.5)
            return

    # Read sensors and decide system state
    t1, h1, ok1, t2, h2, ok2 = bus.read_pair()
    fused = None
    if ok1 or ok2:
        fused, state = voter.fuse_state((t1, h1, ok1), (t2, h2, ok2))
    else:
        state = "fault"

    # Handle button acknowledge
    if btn.pressed():
        acknowledged = True

    # Track consecutive normal states to auto-clear latch
    if state == "normal":
        normal_streak += 1
    else:
        normal_streak = 0

    if normal_streak >= 3:
        acknowledged = False

    # LED + buzzer logic (silent if acknowledged)
    if state == "normal":
        ind.set_normal()
    elif state == "degraded":
        ind.set_degraded_pattern(silent=acknowledged)
    else:
        ind.set_fault_pattern(silent=acknowledged)

    # detect disconnected LED or buzzer pin
    try:
        if state in ("degraded", "fault"):
            if Pin(PIN_LED_R).value() == 0:
                print("Warning: possible LED red pin disconnect")
            if ind.active_low and ind.buzzer.value() == 1:
                print("Warning: possible buzzer pin disconnect")
    except Exception:
        pass

    # test blink
    if force_test:
        ind.test_blink()
        force_test = False

    # 6) Publish telemetry
    alarm_active = (state in ("degraded", "fault")) and (not acknowledged)
    pkt = {
        "device_id": client_id,
        "seq": seq,
        "wifi_status": "ok" if wifi.is_connected() else "down",
        "status": state,
        "buzzer": 1 if alarm_active else 0,
        "buzzer_pin": ind.is_buzzer_active_int(),
    }

    if fused:
        pkt.update({
            "temperature_c": fused[0],
            "humidity_pct": fused[1],
        })
    else:
        pkt.update({
            "temperature_c": None,
            "humidity_pct": None,
        })

    pkt.update({
        "t1": t1, "h1": h1, "ok1": int(ok1),
        "t2": t2, "h2": h2, "ok2": int(ok2),
    })

    publish(mc, pkt)
    mc.check_msg()

    # Feed watchdog
    wdt_guard.feed()

    # Advance sequence / pacing
    seq += 1
    time.sleep(1.0)

# Main
def main():
    wifi.ensure_connected()
    try:
        print("IP:", wifi.ifconfig())
    except Exception:
        pass

    mc.set_callback(on_cmd)
    try:
        mc.connect_and_subscribe([(TOPIC_CMD, 0)])
    except Exception:
        pass

    Startup self-test (LED + buzzer)
    ind.test_blink()
    time.sleep(0.5)

    while True:
        try:
            loop()
        except Exception:
            ind.set_degraded_pattern()
            time.sleep(0.3)

# Run
if __name__ == "__main__":
    main()

