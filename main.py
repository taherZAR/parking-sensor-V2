import machine
import time
import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Pins
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(2, Pin.IN)
BUZZER = PWM(Pin(15), freq=2000, duty=0)
LED = Pin(21, Pin.OUT)
BUTTON = Pin(32, Pin.IN, Pin.PULL_UP)
# WiFi
WIFI_SSID = "Wokwi-GUEST" #just for testing
WIFI_PASS = ""
# MQTT
MQTT_CLIENT_ID = "esp32_taher"
MQTT_BROKER = "broker.hivemq.com" # free testing broker
MQTT_TOPIC = "wokwi" #topic name
# Threshold
DISTANCE_THRESHOLD = 100  # cm (start beeping under this distance)
def connect_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASS)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.2)
    print(" Connected! IP:", sta_if.ifconfig()[0])

def mqtt_publish(distance):
    try:
        message = str(distance).encode()
        client.publish(MQTT_TOPIC, message)
        print("Published:", message)
    except Exception as e:
        print("MQTT publish error:", e)

def pulse_in(pin, timeout=100000):
    timeout *= 1000
    start = time.ticks_us()
    while not pin.value():
        if time.ticks_diff(time.ticks_us(), start) > timeout:
            return -1
    start = time.ticks_us()
    while pin.value():
        if time.ticks_diff(time.ticks_us(), start) > timeout:
            return -1
    return time.ticks_diff(time.ticks_us(), start)

def get_distance():
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    duration = pulse_in(ECHO)
    if duration < 0:
        return float('inf')
    return (duration * 0.0343) / 2

def beep_pattern(distance_cm):
    if distance_cm < DISTANCE_THRESHOLD:
        # Calculate beep speed: closer = faster
        delay = max(0.05, distance_cm / 500)  # from 0.05s to 0.2s for 0-100 cm
        print("Beep Delay:", delay)
        BUZZER.duty(512)
        LED.value(1)
        time.sleep(delay)
        BUZZER.duty(0)
        LED.value(0)
        time.sleep(delay)
    else:
        BUZZER.duty(0)
        LED.value(0)
        time.sleep(0.5)

# MAIN 
connect_wifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.connect()
print("Connected to MQTT broker!")

manual_override = False

while True:
    distance = get_distance()
    print("Distance: %.1f cm" % distance)

    if distance < 400:
        mqtt_publish(distance)

    if BUTTON.value() == 0:
        manual_override = True
        BUZZER.duty(0)
        LED.value(0)
        print("Manual override activated.")
        time.sleep(0.5)

    # Reset override if object is gone
    if manual_override and distance > DISTANCE_THRESHOLD + 5: # plus five for safety buffer
        manual_override = False
        print("Manual override reset.")

    if not manual_override:
        beep_pattern(distance)
    else:
        time.sleep(0.5)
