import matplotlib.pyplot as plt
import time
import RPi.GPIO as GPIO




def init(arr, mode):
    for pin in arr:
        GPIO.setup(pin, mode)


def initialize(DAC, LEDS, v_in, v_out):
    GPIO.setmode(GPIO.BCM)
    init(DAC, GPIO.OUT)
    init(LEDS, GPIO.OUT)
    init([v_in], GPIO.IN)
    init([v_out], GPIO.OUT)


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

# stepping solution


def adc(dac, comp):
    L_VALS = [0 for k in range(8)]
    for i in range(8):
        L_VALS[i] = 1
        set_values(dac, L_VALS)
        time.sleep(0.001)
        if GPIO.input(comp) == GPIO.LOW:
            L_VALS[i] = 0
    time.sleep(0.1)
    print("Binary representation:", *L_VALS, "Decimal", binary2decimal(L_VALS))
    return binary2decimal(L_VALS)


def voltage():
    V_in = 4
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    return adc(dac, V_in)


def show_led(value):
    LEDS_LIST_BCM = [21, 20, 16, 12, 7, 8, 25, 24]
    #LEDS_LIST_BCM.reverse()
    arr = decimal2binary(value)
    set_values(LEDS_LIST_BCM, arr)


def main():
    V_out = 17
    V_in = 4
    leds = [21, 20, 16, 12, 7, 8, 25, 24]
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    initialize(dac, leds, V_in, V_out)
    voltage = []
    try:
        start = time.time()
        GPIO.output(V_out, 1)
        while True:
            res = adc(dac, V_in)
            show_led(res)
            volt = (3.3 * 1000 / 2**8) * int(res)
            voltage.append(volt)
            print("Current voltage is: {} mV".format(
                str(volt)))
            if (volt/3300 >= 0.92):
                break
        #mid = time.time()
        GPIO.output(V_out, 0)
        while True:
            res = adc(dac, V_in)
            show_led(res)
            volt = (3.3 * 1000 / 2**8) * int(res)
            voltage.append(volt)
            print("Current voltage is: {} mV".format(
                str(volt)))
            if (volt/3300 <= 0.02):
                break
        end = time.time()
        
        with open("data.txt", 'w') as f:
            f.write('\n'.join([str(i) for i in voltage]))
        f.close()
        with open("settings.txt", 'w') as f:
            f.write("Discretization freq: "+ str(len(voltage)/(end-start))+ '\n')
            f.write("Step of ADC: {} mV \n".format(3300.0/256.0))
        f.close()
        print("Experiment latency:", str(end-start))
        print("Step of ADC: {} mV".format(3300.0/256.0))
        print("Period of measure:", str((end-start)/len(voltage)))
        plt.plot(voltage)
        plt.show()


    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    finally:
        off_leds(dac)
        off_leds(leds)
        GPIO.output(V_out, 0)
        GPIO.cleanup()


if __name__ == "__main__":
    main()
