#importing required libs
import matplotlib.pyplot as plt
import time
import RPi.GPIO as GPIO



#block of initializing of leds and in/out ports
def init(arr, mode):
    for pin in arr:
        GPIO.setup(pin, mode)


def initialize(DAC, LEDS, v_in, v_out):
    GPIO.setmode(GPIO.BCM)
    init(DAC, GPIO.OUT)
    init(LEDS, GPIO.OUT)
    init([v_in], GPIO.IN)
    init([v_out], GPIO.OUT)

#functions to convert numbers from binary(list of 8 elements 1 and 0) to decimal and against
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def binary2decimal(L_VALS):
    return sum([(2**(7-i)) * L_VALS[i] for i in range(8)])

#functions which set and off leds by using pattern(0 and 1) *values*
def set_values(LEDS, values):
    for i in range(len(LEDS)):
        GPIO.output(LEDS[i], values[i])


def off_leds(LEDS):
    for LED in LEDS:
        GPIO.output(LED, 0)

#show binary representation of vakue in adc
def show_led(value):
    LEDS_LIST_BCM = [21, 20, 16, 12, 7, 8, 25, 24]
    arr = decimal2binary(value)
    set_values(LEDS_LIST_BCM, arr)

# stepping solution of adc for list of 8 binary nums


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

#measure voltage on module
def voltage():
    V_in = 4
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    return adc(dac, V_in)



#main part of program, inits leds, in/out ports
def main():
    #initialize
    V_out = 17
    V_in = 4
    leds = [21, 20, 16, 12, 7, 8, 25, 24]
    dac = [10, 9, 11, 5, 6, 13, 19, 26]
    dac.reverse()
    initialize(dac, leds, V_in, V_out)
    voltage = []
    try:
        #condensator loads
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
        #stop loading, start disloading of condensator
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
        #save got data to file
        with open("data.txt", 'w') as f:
            f.write('\n'.join([str(i) for i in voltage]))
        f.close()
        with open("settings.txt", 'w') as f:
            f.write("Discretization freq: "+ str(len(voltage)/(end-start))+ '\n')
            f.write("Step of ADC: {} mV \n".format(3300.0/256.0))
        f.close()
        #show needed datat on a display
        print("Experiment latency:", str(end-start))
        print("Step of ADC: {} mV".format(3300.0/256.0))
        print("Period of measure:", str((end-start)/len(voltage)))
        #show graphic of voltage
        plt.plot(voltage)
        plt.show()


    except KeyboardInterrupt:
        print("Interrupted by keyboard")
    #off all Rpi GPIO system
    finally:
        off_leds(dac)
        off_leds(leds)
        GPIO.output(V_out, 0)
        GPIO.cleanup()

#protection of using withoout direct program calling
if __name__ == "__main__":
    main()
