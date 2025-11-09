import time
try:
    import ujson as json
except ImportError:
    import json

try:
    from umqtt.simple import MQTTClient
except ImportError:
    raise ImportError("umqtt.simple is required on the device. Upload umqtt/simple.py to /lib.")

TOPIC_DATA = b"ftsms/data"
TOPIC_CMD  = b"ftsms/command"

class MQTTClientWrapper:
    def __init__(self, client_id, broker, port=1883, keepalive=30, username=None, password=None, on_msg=None):
        if isinstance(client_id, str):
            client_id = client_id.encode()
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self.username = username
        self.password = password
        self._on_msg = on_msg
        self._c = None
        self._last_will = None  # (topic, msg, retain, qos)
        self._connected = False

    # Public API
    def set_callback(self, fn):
        self._on_msg = fn
        if self._c:
            self._c.set_callback(self._dispatch)

    def set_last_will(self, topic: bytes, msg: bytes, retain=False, qos=0):
        self._last_will = (topic, msg, retain, qos)

    def connect_and_subscribe(self, topics_qos=None, clean_session=True):
        """Connect (or reconnect) and subscribe to topics_qos list of tuples: [(topic, qos), ...]"""
        self._connect(clean_session=clean_session)
        if topics_qos:
            for tq in topics_qos:
                if isinstance(tq, (list, tuple)) and len(tq) == 2:
                    topic, qos = tq
                else:
                    topic, qos = tq, 0
                self.subscribe(topic, qos=qos)
        return True

    def publish_json(self, topic: bytes, obj: dict, qos=0, retain=False, retry_once=True) -> bool:
        """Publish JSON with simple reconnect on failure. Returns True if sent."""
        payload = json.dumps(obj)
        try:
            self._c.publish(topic, payload, retain=retain, qos=qos)
            return True
        except Exception as e:
            if retry_once:
                try:
                    self._connect(clean_session=False)
                    self._c.publish(topic, payload, retain=retain, qos=qos)
                    return True
                except Exception:
                    return False
            return False

    def subscribe(self, topic: bytes, qos=0):
        self._c.subscribe(topic, qos=qos)

    def check_msg(self):
        """Non-blocking message check; call in main loop frequently."""
        try:
            self._c.check_msg()
        except Exception:
            # Connection likely dropped; try to reconnect
            try:
                self._connect(clean_session=False)
            except Exception:
                pass

    def wait_msg(self):
        """Blocking wait for a message (use sparingly)."""
        self._c.wait_msg()

    def is_connected(self) -> bool:
        return self._connected

    def disconnect(self):
        try:
            self._c.disconnect()
        except Exception:
            pass
        self._connected = False

    # Internal
    def _dispatch(self, topic, msg):
        if self._on_msg:
            try:
                self._on_msg(topic, msg)
            except Exception:
                pass  # keep MQTT loop resilient

    def _connect(self, clean_session=True):
        if self._c is None:
            self._c = MQTTClient(self.client_id, self.broker, port=self.port,
                                 keepalive=self.keepalive, user=self.username, password=self.password,
                                 ssl=False, ssl_params={})
            self._c.set_callback(self._dispatch)
            if self._last_will:
                t, m, r, q = self._last_will
                try:
                    self._c.set_last_will(t, m, retain=r, qos=q)
                except Exception:
                    try:
                        self._c.set_last_will(t, m, retain=r)
                    except Exception:
                        pass
        # Attempt connection with small retry loop
        for _ in range(2):
            try:
                self._c.connect(clean_session=clean_session)
                self._connected = True
                return
            except Exception:
                time.sleep_ms(300)
        # If still here, final attempt (raise on error)
        self._c.connect(clean_session=clean_session)
        self._connected = True
