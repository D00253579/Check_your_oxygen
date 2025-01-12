# Libraries
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv
from time import sleep
import os
import time

red_led = 17
yellow_led = 18
green_led = 27
leds = [red_led, yellow_led, green_led]
buzzer_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
load_dotenv()

GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(yellow_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.LOW)
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
app_channel2 = "Hardware-channel"
subscription = pubnub.channel(app_channel).subscription()
subscription.subscribe()
subscription2 = pubnub.channel(app_channel2).subscription()
publish_result = (
    pubnub.publish().channel(app_channel).message("Hello from CheckYourOxygen").sync()
)


def handle_message(message):
    print("LED MESSAGE:" + message.message)
    temp_notification = str(message.message)
    if temp_notification == '"Oxygen levels are normal "':
        turn_on(green_led)
        pubnub.publish().channel(app_channel2).message("Green LED Activated").sync()
    elif temp_notification == '"Air quality depleting "':
        turn_on(yellow_led)
        pubnub.publish().channel(app_channel2).message("Yellow LED Activated").sync()
    elif (
        temp_notification == '"WARNING! Air Quality Poor "'
        or temp_notification == '"EXTREME TEMPERATURE WARNING ABNORMAL HEAT LEVELS "'
        or temp_notification == '"EXTREME TEMPERATURE WARNING ABNORMAL COLD LEVELS "'
    ):
        turn_on(red_led)
        beep(3)
        pubnub.publish().channel(app_channel2).message(
            "Red LED Activated and buzzer activated"
        ).sync()


def turn_on(pin):
    global leds
    for led in leds:
        if led == pin:
            GPIO.output(pin, GPIO.HIGH)
        else:
            turn_off(led)


def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


def beep(repeat):
    try:
        for i in range(0, repeat):
            for pulse in range(300):
                GPIO.output(buzzer_pin, True)
                time.sleep(0.001)
                GPIO.output(buzzer_pin, False)
                time.sleep(0.001)
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()


def main():
    try:

        subscription2.on_message = lambda message: handle_message(message)
        subscription2.subscribe()

        time.sleep(1)
        while True:
            h, t = dht.read_retry(dht.DHT22, DHT)
            print("Temp={0}*C".format(round(t)))
            pubnub.publish().channel(app_channel).message("{0}".format(round(t))).sync()
            sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
