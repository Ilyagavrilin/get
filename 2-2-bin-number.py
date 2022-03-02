import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])

def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)

def to_bin(value, bits):
    for i in range(8):
        bits[7 - i] = int((value // (2 ** (7 - i))) == 1)
        value = value % (2 ** (7 - i))

def show_num(LEDS, number):
    bits = [0 for i in range(8)]
    to_bin(number, bits)
    set_values(LEDS, bits)
    time.sleep(15)
    off_leds(LEDS)


dac = [10, 9, 11, 5, 6, 13, 19, 26]

number = [random.randint(0, 1) for i in range(len(dac))]
bits = [0 for i in range(len(dac))]

#setup leds
for LED in dac:
    GPIO.setup(LED, GPIO.OUT)

#main part

show_num(dac, )
show_num(dac, 127)
show_num(dac, 64)
show_num(dac, 32)
show_num(dac, 5)
show_num(dac, 0)
GPIO.cleanup()


