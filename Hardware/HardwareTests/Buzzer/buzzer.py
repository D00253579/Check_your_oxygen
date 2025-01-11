import RPi.GPIO as GPIO
import time

buzzer_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.LOW)


def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.02)


while True:
    print("Buzzer activated")
    beep(3)
    time.sleep(1)
