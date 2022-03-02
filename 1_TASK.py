import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)
switch = 0

while True:
    switch = GPIO.input(27)
    GPIO.output(17, switch)
    time.sleep(1)