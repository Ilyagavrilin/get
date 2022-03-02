import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
aux = [22, 23, 27, 18, 15, 14, 3, 2]
condition = [0 for i in range(8)]
#setup leds
for LED in leds:
    GPIO.setup(LED, GPIO.OUT)
for LED in aux:
    GPIO.setup(LED, GPIO.IN)



def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])

def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)

def get_values(PINS, values):
    for i in range(len(PINS)):
        values[i] = GPIO.input(PINS[i])


#main
while True:
    get_values(aux, condition)
    set_values(leds, condition)