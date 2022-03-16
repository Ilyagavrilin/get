import RPi.GPIO as GPIO
import time


def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)

def main():
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    GPIO.setmode(GPIO.BCM)
    #setup leds
    for LED in dac:
        GPIO.setup(LED, GPIO.OUT)
    try:
        val = input("Type period of saw (in milliseconds):")
        if (val.lower() == 'q'):
            raise Exception
        else:
            val = float(val)

        if (val <= 0):
            raise ValueError("Incorrect range") 
        while True:
            for i in range(256):
                bin = decimal2binary(i)
                set_values(dac, bin)
                time.sleep(val/(256*2))
            for i in range(0, 256, -1):
                bin = decimal2binary(i)
                set_values(dac, bin)
                time.sleep(val/(256*2))
        
         
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    except ValueError as err:
        print("Value incorrect:", err)
    except Exception:
        print("Interrupted by user")
    finally:
        off_leds(dac)
        GPIO.cleanup()
    return

if __name__ == "__main__":
    main()
