import numpy as np
import matplotlib.pyplot as plt 
import math 

SAMPLING_FREQUENCY = 1024
SAMPLING_PERIOD = 1 / SAMPLING_FREQUENCY
NYQUIST_FRECUENCY = SAMPLING_FREQUENCY // 2
TOTAL_TIME = 1            
NUMBER_OF_SAMPLES = TOTAL_TIME * SAMPLING_FREQUENCY          
BASE_FREQUENCY = 1 // TOTAL_TIME

def generateSignal():
    time_array = np.arange(0, TOTAL_TIME, SAMPLING_PERIOD)
    signal_array = np.zeros(NUMBER_OF_SAMPLES)

    signal_array[0 : NUMBER_OF_SAMPLES // 2] = time_array[0 : NUMBER_OF_SAMPLES // 2]
    signal_array[NUMBER_OF_SAMPLES // 2 : NUMBER_OF_SAMPLES] = time_array[0 : NUMBER_OF_SAMPLES // 2]

    # Signal transforms to match example
    signal_array *= 2
    signal_array -= .5

    X = np.abs(np.fft.fft(signal_array))

    # Frequency vector
    f = (SAMPLING_FREQUENCY)*(np.arange(NUMBER_OF_SAMPLES)/NUMBER_OF_SAMPLES)
    plt.figure("Signal Frequency Spectrum")
    plt.plot(f,X)
    plt.show()

    return time_array, signal_array

if __name__ == "__main__":
    x, y = generateSignal()
    # Plots
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Time(sec)',fontsize=14)
    plt.ylabel('signal_array(t)',fontsize=14)
    plt.show()