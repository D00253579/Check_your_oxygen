# Libraries
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv
from time import sleep
import os

red_led = 17
yellow_led = 18
green_led = 27
leds = [red_led, yellow_led, green_led]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
load_dotenv()

GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(yellow_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)
# Set DATA pin
DHT = 4


class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f"Status: \n{status.category.name}")


config = PNConfiguration()
config.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
config.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
config.user_id = os.getenv("ADMIN_GOOGLE_ID")
pubnub = PubNub(config)
pubnub.add_listener(Listener())
app_channel = "Temp-channel"
subscription = pubnub.channel(app_channel).subscription()
subscription.subscribe()
publish_result = (
    pubnub.publish().channel(app_channel).message("Hello from CheckYourOxygen").sync()
)


def turn_on(pin):
    global leds
    for led in leds:
        if led == pin:
            GPIO.output(pin, GPIO.HIGH)
        else:
            turn_off(led)


def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


def main():
    try:
        while True:
            # Read Temp and Hum from DHT22
            h, t = dht.read_retry(dht.DHT22, DHT)
            # Print Temperature and Humidity on Shell window
            print("Temp={0}*C".format(round(t)))
            pubnub.publish().channel(app_channel).message("{0}".format(round(t))).sync()
            sleep(5)  # Wait 5 seconds and read again
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
