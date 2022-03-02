import RPi.GPIO as GPIO
import time

def light_time(LED_NAME, delatter):
    GPIO.output(LED_NAME, 1)
    time.sleep(delatter)
    GPIO.output(LED_NAME, 0)
    return


GPIO.setmode(GPIO.BCM)
LEDS_LIST_BCM = [21, 20, 16, 12, 7, 8, 25, 24]



for LED in LEDS_LIST_BCM:
    GPIO.setup(LED, GPIO.OUT)

for i in range(3):
    for LED in LEDS_LIST_BCM: light_time(LED, 0.2)
    

for LED in LEDS_LIST_BCM:
    GPIO.output(LED, 0)
GPIO.cleanup()
