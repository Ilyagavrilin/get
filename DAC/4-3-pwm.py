import RPi.GPIO as GPIO


def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])


def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)


def main():
    GPIO.setmode(GPIO.BCM)
    LED = 7
    GPIO_PWM = 2
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(GPIO_PWM, GPIO.OUT)
    try:
        mode = int(input("Choose LED - 1 or PWM - 0:"))
        if (mode == 1):
            led_pwm = GPIO.PWM(LED, 1000)
        else:
            led_pwm = GPIO.PWM(GPIO_PWM, 1000)

        led_pwm.start(0)

        while True:
            val = input("Type duty (in percents):")
            if (val.lower() == 'q'):
                raise Exception
            else:
                val = float(val)
            if mode == 1:
                pass
            led_pwm.ChangeDutyCycle(val)

        if (val < 0 or val > 100):
            raise ValueError("Incorrect range")
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    except ValueError as err:
        print("Value incorrect:", err)
    except Exception:
        print("Interrupted by user")
    finally:
        led_pwm.stop()
        off_leds([LED, GPIO_PWM])
        GPIO.cleanup()
    return


if __name__ == "__main__":
    main()
