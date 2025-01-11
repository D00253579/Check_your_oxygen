# Libraries
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from time import sleep

red_led = 17
yellow_led = 18
green_led = 27
leds = [red_led, yellow_led, green_led]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(yellow_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)
# Set DATA pin
DHT = 4


def turn_on(pin):
    global leds
    for led in leds:
        if led == pin:
            GPIO.output(pin, GPIO.HIGH)
        else:
            turn_off(led)


def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


while True:
    # Read Temp and Hum from DHT22
    h, t = dht.read_retry(dht.DHT22, DHT)
    # Print Temperature and Humidity on Shell window
    print(h)
    if t > 18:
        turn_on(green_led)
    print("Temp={0:0.1f}*C".format(t))
    sleep(5)  # Wait 5 seconds and read again
