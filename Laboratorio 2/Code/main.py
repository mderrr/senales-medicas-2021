import os
os.chdir(os.getcwd() + "/Laboratorio 2/Code/")

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from signal_generator import generateSignal

SAMPLING_FREQUENCY = 1024
SAMPLING_PERIOD = 1 / SAMPLING_FREQUENCY
NYQUIST_FRECUENCY = SAMPLING_FREQUENCY // 2
TOTAL_TIME = 1            
NUMBER_OF_SAMPLES = TOTAL_TIME * SAMPLING_FREQUENCY          
BASE_FREQUENCY = 1 // TOTAL_TIME
NUMBER_OF_COMPONENTS = 24

time_array, base_signal_array = generateSignal()


points_to_display = []

# PUNTO 1
def displayFirstPoint():
    def applyFourierTransform(signal_array, number_of_components, number_of_samples):
        array = np.fft.fft(signal_array)
        blank_index = np.arange(number_of_components, number_of_samples - (number_of_components - 1))
        array[blank_index] = 0 + 0j

        return array

    def ifftReconstruct(signal_array, number_of_components, number_of_samples):
        transformed_signal = applyFourierTransform(signal_array, number_of_components, number_of_samples)
        reconstructed_signal = np.fft.ifft(transformed_signal)

        return np.real(reconstructed_signal)

    def ecuationReconstruct(signal_array, time_array, number_of_samples, number_of_components):
        reconstructed_signal = np.zeros(number_of_samples)

        for m in range(number_of_components):
            f = m * BASE_FREQUENCY
            a = (2 / number_of_samples) * np.sum(signal_array * (np.cos(2 * np.pi * f * time_array)))
            b = (2 / number_of_samples) * np.sum(signal_array * (np.sin(2 * np.pi * f * time_array)))
            X_magnitude = np.sqrt((a ** 2) + (b ** 2))
            X_phase = -math.atan2(b, a)

            reconstructed_signal += X_magnitude * np.cos(2 * np.pi * f * time_array + X_phase)
            reconstructed_signal[m] += np.mean(signal_array)

        return reconstructed_signal

    def plotSignal(time_array, signal_array, base_signal_array, method="IFFT"):
        plt.figure("Signal Reconstruction Via {}".format(method))
        plt.plot(time_array, signal_array)
        plt.plot(time_array, base_signal_array, linestyle="dashed")
        plt.xlabel("Time(sec)", fontsize=14)
        plt.ylabel("x(t)", fontsize=14)
        plt.title("{} components reconstruction using {}".format(NUMBER_OF_COMPONENTS, method), fontsize=14)

    ifft_reconstructed_signal = ifftReconstruct(base_signal_array, NUMBER_OF_COMPONENTS, NUMBER_OF_SAMPLES)
    ecuation_reconstructed_signal = ecuationReconstruct(base_signal_array, time_array, NUMBER_OF_SAMPLES, NUMBER_OF_COMPONENTS)

    plotSignal(time_array, ecuation_reconstructed_signal, base_signal_array, method="Ecuation")
    plotSignal(time_array, ifft_reconstructed_signal, base_signal_array)
    plt.show()

# PUNTO 2
def displaySecondPoint():
    signal1_csv = pd.read_csv("../signal1.csv")
    signal_array = signal1_csv["Signal"]
    
    sampling_frequency = 1000    
    number_of_samples = len(signal_array)
    subplot_size_x, subplot_size_y = (2, 3)

    transformed_signal = np.fft.fft(signal_array)
    transformed_signal = np.abs(transformed_signal)

    def createSubPlots(zero_padding=False):
        figure, plots = plt.subplots(subplot_size_x, subplot_size_y, num="Frequency Spectrums")

        for x in range(subplot_size_x):
            for y in range(subplot_size_y):
                current_plot = plots[x, y]
                one_dimensional_index = (x * subplot_size_y) + y
                frequencie_divider = 1 * pow(2, one_dimensional_index)
                relative_number_of_samples = number_of_samples // frequencie_divider
                relative_signal = np.zeros(number_of_samples if zero_padding else relative_number_of_samples)

                if zero_padding:
                    relative_frequency = (sampling_frequency) * (np.arange(number_of_samples) / (number_of_samples))
                else:
                    relative_frequency = (sampling_frequency // frequencie_divider) * (np.arange(relative_number_of_samples) / (relative_number_of_samples))

                relative_signal[0 : relative_number_of_samples] = transformed_signal[0 : relative_number_of_samples]

                current_plot.plot(relative_frequency, relative_signal)
                current_plot.set_title("From 1 to {}".format(relative_number_of_samples))

        figure.suptitle("Zero Padding: {}".format("Enabled" if zero_padding else "Disabled"))
        plt.show()

    createSubPlots()
    createSubPlots(True)

# Point 3
def displayThirdPoint():

    
#points_to_display.append(displayFirstPoint)
points_to_display.append(displaySecondPoint)

for e in points_to_display:
    e()