import RPi.GPIO as GPIO

red_led = 17
yellow_led = 18
green_led = 27
leds = [red_led, yellow_led, green_led]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(yellow_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_led, GPIO.OUT, initial=GPIO.LOW)


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
            coffee_temp = int(
                input(
                    "What temperature is it? (31 for red, 18 for green, 25 for yellow): "
                )
            )

            if coffee_temp > 30:
                turn_on(red_led)

            elif coffee_temp < 20:
                turn_on(green_led)

            else:
                turn_on(yellow_led)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
