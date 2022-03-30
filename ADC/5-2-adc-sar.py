import RPi.GPIO as GPIO
import time

def initialize(arr, mode):
    for pin in arr:
        GPIO.setup(pin, mode)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def binary2decimal(L_VALS):
    return sum([(2**(7-i)) * L_VALS[i] for i in range(8)])

def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])

def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)
#stepping solution
def adc(dac, comp):
    L_VALS = [0 for k in range(8)]
    for i in range(8):
        L_VALS[i] = 1
        set_values(dac, L_VALS)
        time.sleep(0.0001)
        if GPIO.input(comp) == GPIO.LOW:
            L_VALS[i] = 0
    time.sleep(0.1)
    print("Binary representation:", *L_VALS, "Decimal", binary2decimal(L_VALS))
    return binary2decimal(L_VALS)

def main():
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    comp = 4
    troyka = 17
    GPIO.setmode(GPIO.BCM)
    initialize(dac, GPIO.OUT)
    GPIO.setup(comp, GPIO.IN)
    GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
    try:
        while True:
            res = adc(dac, comp)
            print("Current voltage is: {} mV".format((3.3 * 1000 / 2**8) * int(res)))

        
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    finally:
        off_leds(dac)
        GPIO.output(troyka, 0)
        GPIO.cleanup()



if __name__ == "__main__":
    main()