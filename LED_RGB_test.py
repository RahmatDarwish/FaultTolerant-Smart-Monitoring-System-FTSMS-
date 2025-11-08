from machine import Pin, PWM
import time

LED_R = Pin(16, Pin.OUT)
LED_G = Pin(15, Pin.OUT)
LED_B = Pin(14, Pin.OUT)

def off():
    LED_R.value(0); LED_G.value(0); LED_B.value(0)

def color(r,g,b):  # r,g,b = 0/1
    LED_R.value(1 if r else 0)
    LED_G.value(1 if g else 0)
    LED_B.value(1 if b else 0)

print("RGB CNT1 test")

# Quick color sanity check
for c in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(0,1,1),(1,0,1),(1,1,1)]:
    color(*c); time.sleep(1)
off()

# 10s on (white), 10s off loop
while True:
    print("ON 10s");  color(1,1,1); time.sleep(5)
    print("OFF 10s"); off();        time.sleep(2)
