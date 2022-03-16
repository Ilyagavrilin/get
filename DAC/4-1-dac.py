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
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    GPIO.setmode(GPIO.BCM)
    #setup leds
    for LED in dac:
        GPIO.setup(LED, GPIO.OUT)
    try:
        val = input("Type number from 0 to 255(or q to quit):")
        if (val.lower() == 'q'):
            raise Exception
        else:
            val = int(val)

        if (val < 0 or val > 255):
            raise ValueError("Incorrect range")
        
        bin = decimal2binary(val)
        print("Voltage: {:.5f} V".format(3.3*val/255.0))
        print("Binary representation:", *bin)
        set_values(dac, bin)
        if (input("Press any key to stop:")): 
            raise Exception   
         
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    except ValueError as err:
        print("Value incorrect:", err)
    except Exception:
        print("Interrupted by user")
    finally:
        off_leds(dac)
        GPIO.cleanup()


if __name__ == "__main__":
    main()