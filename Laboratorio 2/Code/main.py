import os
os.chdir(os.getcwd() + "/Laboratorio 2/Code/")

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from statistics import mean
from signal_generator import generateSignal

POINT_2B_RESPONSE = ""

points_to_display = []

# PUNTO 1
def firstPoint():
    SAMPLING_FREQUENCY = 1024
    SAMPLING_PERIOD = 1 / SAMPLING_FREQUENCY
    TOTAL_TIME = 1            
    NUMBER_OF_SAMPLES = TOTAL_TIME * SAMPLING_FREQUENCY          
    BASE_FREQUENCY = 1 // TOTAL_TIME
    NUMBER_OF_COMPONENTS = 24

    def generateSignal(total_time, sampling_frequency):
        sampling_period = 1 / sampling_frequency
        number_of_samples = total_time * sampling_frequency
        time_array = np.arange(0, total_time, sampling_period)
        print(number_of_samples)
        signal_array = np.zeros(number_of_samples)

        signal_array[0 : number_of_samples // 2] = time_array[0 : number_of_samples // 2]
        signal_array[number_of_samples // 2 : number_of_samples] = time_array[0 : number_of_samples // 2]

        # Signal transforms to match example
        signal_array *= 2
        signal_array -= .5

        transformed_signal_array = np.abs(np.fft.fft(signal_array))
        half_transformed_signal_array = transformed_signal_array[: number_of_samples // 2]
        frequency_array = (sampling_frequency // 2) * (np.arange(number_of_samples // 2) / (number_of_samples // 2))

        figure, (subplot_original, subplot_transformed) = plt.subplots(ncols=2, num="Punto 1)")
        figure.suptitle("Sawtooth Signal")
        subplot_original.plot(time_array, signal_array)
        subplot_original.set_xlabel("Time (s)")
        subplot_original.set_title("Signal")
        subplot_transformed.plot(frequency_array, half_transformed_signal_array)
        subplot_transformed.set_xlabel("Frequency (Hz)")
        subplot_transformed.set_title("Frequency Spectrum")
        plt.show()

        return time_array, signal_array

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

    def plotSignal(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array):
        figure, (subplot_ifft, subplot_ecuation) = plt.subplots(ncols=2, num="Punto 1)")
        figure.suptitle("Signal Reconstruction")
        figure.text(0.5, 0.04, "Time (s)", ha='center')
        figure.text(0.04, 0.5, "x(t)", va='center', rotation='vertical')
        subplot_ifft.plot(time_array, ifft_reconstructed_signal)
        subplot_ifft.plot(time_array, base_signal_array, linestyle="dashed")
        subplot_ifft.set_title("Using IFFT")
        subplot_ecuation.plot(time_array, ecuation_reconstructed_signal)
        subplot_ecuation.plot(time_array, base_signal_array, linestyle="dashed")
        subplot_ecuation.set_title("Using Ecuation")
        plt.show()


    time_array, base_signal_array = generateSignal(TOTAL_TIME, SAMPLING_FREQUENCY)

    ifft_reconstructed_signal = ifftReconstruct(base_signal_array, NUMBER_OF_COMPONENTS, NUMBER_OF_SAMPLES)
    ecuation_reconstructed_signal = ecuationReconstruct(base_signal_array, time_array, NUMBER_OF_SAMPLES, NUMBER_OF_COMPONENTS)

    plotSignal(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array)
    plt.show()

# PUNTO 2
def secondPoint():
    signal1_csv = pd.read_csv("../signal1.csv")
    signal_array = signal1_csv["Signal"]
    sampling_frequency = 1000    
    number_of_samples = len(signal_array)
    subplot_size_x, subplot_size_y = (2, 3)

    transformed_signal = np.abs(np.fft.fft(signal_array))
    transformed_signal = transformed_signal[:number_of_samples // 2]
    base_frequency = (sampling_frequency // 2) * (np.arange(number_of_samples // 2) / (number_of_samples // 2))

    def displayOriginal():
        plt.figure("Punto 2a)")
        plt.title("Complete Frequency Spectrum")
        plt.xlabel("Frequency (Hz)")
        plt.plot(base_frequency, transformed_signal)
        plt.show()

    def displayPortionedFrequencies(zero_padding=False):
        '''figure, plots = plt.subplots(subplot_size_x, subplot_size_y, num="Punto 2b)")

        for x in range(subplot_size_x):
            for y in range(subplot_size_y):
                current_plot = plots[x, y]
                one_dimensional_index = (x * subplot_size_y) + y
                frequency_divider = 1 * pow(2, one_dimensional_index)
                relative_number_of_samples = number_of_samples // frequency_divider
                relative_signal = np.zeros(number_of_samples if zero_padding else relative_number_of_samples)

                if zero_padding:
                    relative_frequency = base_frequency #(sampling_frequency) * (np.arange(number_of_samples) / (number_of_samples))
                else:
                    relative_frequency = (sampling_frequency // frequency_divider) * (np.arange(relative_number_of_samples) / (relative_number_of_samples))

                relative_signal[0 : relative_number_of_samples] = transformed_signal[0 : relative_number_of_samples]

                current_plot.plot(relative_frequency, relative_signal)
                current_plot.set_title("From 1 to {}".format(relative_number_of_samples))

        figure.suptitle("Portioned Frequency Spectrums With Zero Padding {}".format("Enabled" if zero_padding else "Disabled"))
        plt.show()'''

        figure, plots = plt.subplots(subplot_size_x, subplot_size_y, num="Punto 2b){}".format(zero_padding))

        for x in range(subplot_size_x):
            for y in range(subplot_size_y):
                current_plot = plots[x, y]
                one_dimensional_index = (x * subplot_size_y) + y
                frequency_divider = 1 * pow(2, one_dimensional_index)
                relative_number_of_samples = number_of_samples // frequency_divider
                relative_signal = np.zeros((number_of_samples) if zero_padding else relative_number_of_samples)
                print("LEN REALTI", len(relative_signal))
                relative_signal[:relative_number_of_samples] = signal_array[:relative_number_of_samples]

                if zero_padding:
                    #relative_frequency = base_frequency #(sampling_frequency) * (np.arange(number_of_samples) / (number_of_samples))

                    #relative_signal[:relative_number_of_samples] = signal_array[:relative_number_of_samples]
                    relative_frequency = base_frequency#(sampling_frequency // 2) * (np.arange(number_of_samples // 2) / (number_of_samples // 2))
                    
                else:
                    #relative_frequency = (sampling_frequency // frequency_divider) * (np.arange(relative_number_of_samples) / (relative_number_of_samples))
                    relative_frequency = (sampling_frequency // 2) * (np.arange(relative_number_of_samples // 2) / (relative_number_of_samples // 2))

                    #relative_signal = signal_array[:relative_number_of_samples]
                #relative_signal[0 : relative_number_of_samples] = transformed_signal[0 : relative_number_of_samples]
                #relative_signal = signal_array[:int(len(signal_array) / frequency_divider)]
                print("LEN REALTI FREQ", len(relative_frequency))
                print("AT ", one_dimensional_index)#, relative_signal)
                transformed_relative_signal = np.abs(np.fft.fft(relative_signal))
                if not zero_padding:
                    transformed_relative_signal = transformed_relative_signal[:relative_number_of_samples // 2]
                else:
                    transformed_relative_signal = transformed_relative_signal[:number_of_samples // 2]

                current_plot.plot(relative_frequency, transformed_relative_signal)
                current_plot.set_title("From 1 to {}".format(relative_number_of_samples))

        figure.suptitle("Portioned Frequency Spectrums With Zero Padding {}".format("Enabled" if zero_padding else "Disabled"))
        plt.show()

    displayOriginal()
    displayPortionedFrequencies()
    
    #print(POINT_2B_RESPONSE)
    displayPortionedFrequencies(True)
    

# Point 3
def thirdPoint():
    ecg_csv = pd.read_csv("../ecg_1min.csv")
    ecg_peaks_csv = pd.read_csv("../ecg_1min_rpeaks.csv")
    ecg_array = ecg_csv["ECG"]
    ecg_peaks_array = ecg_peaks_csv["R peaks"]
    sampling_frequency = 250
    sampling_period = 1 / sampling_frequency
    sampling_cutting_point = 20
    sampling_divider = sampling_frequency / sampling_cutting_point
    number_of_samples = len(ecg_array)
    zoomed_number_of_samples = number_of_samples // sampling_divider
    zoomed_ecg_array = []

    def displayFrequencies():
        transformed_ecg_array = np.abs(np.fft.fft(ecg_array))
        zoomed_ecg_array = transformed_ecg_array[0: int(zoomed_number_of_samples)]

        frequency_array = (sampling_frequency) * (np.arange(number_of_samples) / number_of_samples)
        zoomed_frequency_array = (sampling_frequency / sampling_divider)*(np.arange(zoomed_number_of_samples) / zoomed_number_of_samples)


        figure, (subplot_original, subplot_zoomed) = plt.subplots(1, 2, num="Frequency Spectrums")
        figure.suptitle("ECG Frequency Spectrums")
        subplot_original.plot(frequency_array, transformed_ecg_array)
        subplot_original.set_title("Complete Frequency")
        subplot_zoomed.plot(zoomed_frequency_array, zoomed_ecg_array)
        subplot_zoomed.set_title("Zoomed In Frequency")

        plt.show()

        # ================================================== Hallar frecuencia cardiaca ================================================== #

        # Si tomamos la posicion donde esta el valor maximo de la funcion transformada
        max_frecuency_position = np.argmax(transformed_ecg_array)

        # Y la usamos como indice para la lista de frecuencias, obtenemos el valor de frecuencia mas parecido a nuestro ECG, en este caso:
        max_frecuency_value = frequency_array[max_frecuency_position]
        print("Most similar frecuency value: {}Hz".format(max_frecuency_value))

        # Ahora si tomamos la frecuencia, la cual esta en Hz osea ciclos por segundo, y la multiplicamos por 60s nos va a dar un valor en
        # ciclos por minuto, lo cual es exactamente lo que nesecitamos para la frecuencia cardiaca que esta dada en latidos por minuto:
        heart_rate = max_frecuency_value * 60
        print("The patient's heart rate is: {}bpm".format(round(heart_rate)))

        

    previous_peak = 0
    peak_periods=[]

    '''for peak in ecg_peaks_array:
        current_peak = (peak * sampling_period) - previous_peak
        peak_periods.append(current_peak)
        previous_peak = (peak * sampling_period)
        print("PEAK * PEROS: ", current_peak)

    print("MEAN: ", mean(peak_periods))
    print("MEAN LPM: ", mean(peak_periods) * 60)
    print(len(ecg_peaks_array))'''

    displayFrequencies()



#points_to_display.append(firstPoint)
points_to_display.append(secondPoint)
#points_to_display.append(thirdPoint)


for e in points_to_display:
    e()