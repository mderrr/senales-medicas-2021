import os
os.chdir(os.getcwd() + "/Laboratorio 2/Code/")

import math
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from statistics import mean
from signal_generator import generateSignal

POINT_2B_RESPONSE = ("RESPUESTA 2B: Al reducir en número de valores en la señal, esta pierde resolución y se hace más complicado diferenciar cuál de las frecuencias tiene "
                    "un gran parecido con la señal, hasta que al final pareciese que hay más de dos frecuencias dominantes.\nEste efecto es resultado de que al tomar "
                    "porciones cada vez más pequeñas de la señal, estamos efectivamente reduciendo la cantidad de puntos que tomamos en cuenta, haciendo que valores de "
                    "frecuencia que en la señal original no tenían tanta presencia, se vean más representados debido a la menor cantidad de datos en total.")
POINT_2C_RESPONSE = ("RESPUESTA 2C: Al hacer uso del zero padding se puede ver que la señal parece contener más valores y parece tener la habilidad de mantener una resolución"
                    " razonable por más tiempo, que si no usáramos este método.\nEsto hace que sea más fácil reconocer las dos frecuencias dominantes de la señal tomando "
                    "porciones más pequeñas de esta, sin embargo, no es infalible ya que al final presenta los mismos problemas que en el ejemplo anterior.")
POINT_3A_RESPONSE = ("RESPUESTA 3A: Si tomamos el índice de la posición donde está el valor máximo de la función transformada, en este caso: {}.\nY luego la usamos como "
                    "índice para la lista de frecuencias, obtendremos el valor de frecuencia más parecido a nuestro ECG, en este caso: ~{}Hz\nAhora si tomamos la frecuencia, "
                    "la cual está en Hz ósea ciclos por segundo, y la multiplicamos por 60s nos va a dar un valor en ciclos por minuto, lo cual es exactamente lo que "
                    "necesitamos para la frecuencia cardiaca que esta dada en latidos (ciclos) por minuto.\nY esto nos da como respuesta una frecuencia cardiaca de: {} Lpm")
POINT_3B_RESPONSE = ("RESPUESTA 3B: Los valores obtenidos en el numeral 2 y 3 son similares y en mi opinión la respuesta a la pregunta de si la medición de la frecuencia "
                    "cardiaca usando el espectro de frecuencia es confiable, depende del uso que se le quiera dar a el resultado.\nPor ejemplo, si se quiere usar en una "
                    "aplicación de fitness que te diga tu frecuencia cardiaca mientras te ejercitas, el rango de error de la medición no es tan importante y por lo tanto el "
                    "uso del espectro sería aceptable, aunque no sea el más acertado, mientras que, en un ambiente clínico el margen de error de este método podría ser "
                    "inaceptable y hasta peligroso por lo cual se debería usar la alternativa.\nSin embargo, a mi parecer es siempre mejor usar el método del numeral 3 ya "
                    "que, con este además de obtenerse un resultado más acertado, no es tan afectado por la fluctuación en el cambio del periodo entre latidos, ya que cada "
                    "uno de estos se mide y luego se promedia. En cambio, en el método del espectro, se toma la frecuencia más parecida y se calculan las pulsaciones por "
                    "minuto en base a esta, haciendo parecer a la señal completamente estable y sin fluctuaciones, lo cual no es la realidad de cómo son los latidos del corazón.")
        
WINDOWS_PLATFORM_NAME = "Windows"

WINDOWS_CLEAR = "cls"
UNIX_CLEAR = "clear"

SPACE = " "
COMMA = ", "
COMMA_ELLIPSIS = COMMA + "..."

FIRST_POINT, SECOND_POINT, THIRD_POINT = (0, 1, 2)


SAMPLING_FREQUENCIES = [1024]
TOTAL_TIMES = [1]

RECONSTRUCTION_COMPONENTS = 24

def clear():
    os.system(WINDOWS_CLEAR if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_CLEAR)

def printResponse(response):
    clear()
    print(response)

def printShortList(list, list_title, item_format, list_end=10):
            print(list_title, end=SPACE)

            for heart_rate in list[:list_end]:
                print(item_format.format(round(heart_rate)), end=COMMA)

            print(item_format.format(round(list[list_end])) + COMMA_ELLIPSIS)

def firstPoint():
    sampling_frequency = SAMPLING_FREQUENCIES[FIRST_POINT]
    total_time = TOTAL_TIMES[FIRST_POINT]          
    number_of_samples = total_time * sampling_frequency          
    base_frequency = 1 // total_time

    def generateSignal(sampling_frequency, total_time, number_of_samples):
        sampling_period = 1 / sampling_frequency
        time_array = np.arange(0, total_time, sampling_period)
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

    def ecuationReconstruct(number_of_samples, number_of_components, base_frequency, signal_array, time_array):
        reconstructed_signal = np.zeros(number_of_samples)

        for m in range(number_of_components):
            f = m * base_frequency
            a = (2 / number_of_samples) * np.sum(signal_array * (np.cos(2 * np.pi * f * time_array)))
            b = (2 / number_of_samples) * np.sum(signal_array * (np.sin(2 * np.pi * f * time_array)))
            X_magnitude = np.sqrt((a ** 2) + (b ** 2))
            X_phase = -math.atan2(b, a)

            reconstructed_signal += X_magnitude * np.cos(2 * np.pi * f * time_array + X_phase)
            reconstructed_signal[m] += np.mean(signal_array)

        return reconstructed_signal

    def plotSignal(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array, number_of_components):
        figure, (subplot_ifft, subplot_ecuation) = plt.subplots(ncols=2, num="Punto 1)")
        figure.suptitle("{} Point Signal Reconstruction".format(number_of_components))
        figure.text(0.5, 0.04, "Time (s)", ha='center')
        figure.text(0.04, 0.5, "x(t)", va='center', rotation='vertical')
        subplot_ifft.plot(time_array, ifft_reconstructed_signal)
        subplot_ifft.plot(time_array, base_signal_array, linestyle="dashed")
        subplot_ifft.set_title("Using IFFT")
        subplot_ecuation.plot(time_array, ecuation_reconstructed_signal)
        subplot_ecuation.plot(time_array, base_signal_array, linestyle="dashed")
        subplot_ecuation.set_title("Using Ecuation")
        plt.show()


    time_array, base_signal_array = generateSignal(sampling_frequency, total_time, number_of_samples)

    ifft_reconstructed_signal = ifftReconstruct(base_signal_array, RECONSTRUCTION_COMPONENTS, number_of_samples)
    ecuation_reconstructed_signal = ecuationReconstruct(number_of_samples, RECONSTRUCTION_COMPONENTS, base_frequency, base_signal_array, time_array)

    plotSignal(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array, RECONSTRUCTION_COMPONENTS)
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
        figure, plots = plt.subplots(subplot_size_x, subplot_size_y, num="Punto 2{})".format("c" if zero_padding else "b"))

        for x in range(subplot_size_x):
            for y in range(subplot_size_y):
                current_plot = plots[x, y]
                one_dimensional_index = (x * subplot_size_y) + y
                frequency_divider = 1 * pow(2, one_dimensional_index)
                relative_number_of_samples = number_of_samples // frequency_divider
                relative_signal = np.zeros((number_of_samples) if zero_padding else relative_number_of_samples)
                relative_signal[:relative_number_of_samples] = signal_array[:relative_number_of_samples]

                if zero_padding:
                    relative_frequency = base_frequency
                    
                else:
                    relative_frequency = (sampling_frequency // 2) * (np.arange(relative_number_of_samples // 2) / (relative_number_of_samples // 2))

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

    printResponse(POINT_2B_RESPONSE)
    displayPortionedFrequencies()
   
    printResponse(POINT_2C_RESPONSE)
    displayPortionedFrequencies(True)
    
# Point 3
def thirdPoint():
    ecg_csv = pd.read_csv("../ecg_1min.csv")
    ecg_peaks_csv = pd.read_csv("../ecg_1min_rpeaks.csv")
    ecg_array = ecg_csv["ECG"]
    ecg_peaks_array = ecg_peaks_csv["R peaks"]
    sampling_frequency = 250
    
    sampling_cutting_point = 20
    sampling_divider = sampling_frequency / sampling_cutting_point
    number_of_samples = len(ecg_array)
    zoomed_number_of_samples = number_of_samples // sampling_divider
    zoomed_ecg_array = []

    def displayFrequencies():
        transformed_ecg_array = np.abs(np.fft.fft(ecg_array))
        half_transformed_ecg_array = transformed_ecg_array[:number_of_samples // 2]
        zoomed_ecg_array = transformed_ecg_array[0: int(zoomed_number_of_samples)]

        frequency_array = (sampling_frequency) * (np.arange(number_of_samples) / number_of_samples)
        half_frequency_array = (sampling_frequency / 2) * (np.arange(number_of_samples / 2) / number_of_samples / 2)
        zoomed_frequency_array = (sampling_frequency / sampling_divider)*(np.arange(zoomed_number_of_samples) / zoomed_number_of_samples)

        figure, (subplot_original, subplot_zoomed) = plt.subplots(1, 2, num="Punto 3a)")
        figure.suptitle("ECG Frequency Spectrums")
        subplot_original.plot(half_frequency_array, half_transformed_ecg_array)
        subplot_original.set_title("Complete Frequency")
        subplot_zoomed.plot(zoomed_frequency_array, zoomed_ecg_array)
        subplot_zoomed.set_title("Zoomed In Frequency")

        # Heart Rate
        max_frecuency_position = np.argmax(transformed_ecg_array)
        max_frecuency_value = frequency_array[max_frecuency_position]
        heart_rate = max_frecuency_value * 60

        printResponse(POINT_3A_RESPONSE.format(max_frecuency_position, round(max_frecuency_value, 2), round(heart_rate)))
        plt.show()

    def getIntantHeartRate():
        sampling_period = 1 / sampling_frequency
        previous_peak = 0
        instant_heart_rate_array=[]

        '''for peak in ecg_peaks_array:
            current_peak_period = (peak * sampling_period) - previous_peak
            
            
            current_heart_rate = current_peak_period * 60

            instant_heart_rate_array.append(current_heart_rate)

            previous_peak = (peak * sampling_period)
            print("PERIOD: ", previous_peak)
            print("INST HR: ", current_heart_rate)'''

        for i in range(len(ecg_peaks_array)):
            try:
                peak_difference = ecg_peaks_array[i] - ecg_peaks_array[i - 1]
            except KeyError:
                peak_difference = ecg_peaks_array[i]

            peak_period = peak_difference * sampling_period
            instant_heart_rate = (1 / peak_period) * 60

            instant_heart_rate_array.append(instant_heart_rate)

        

        printResponse(POINT_3B_RESPONSE)
        printShortList(instant_heart_rate_array, "\nFrecuencias cardiacas instantaneas:", "{} Lpm")
        print("Frecuencia cardiaca promedio:", round(mean(instant_heart_rate_array)))
        
    displayFrequencies()
    getIntantHeartRate()


clear()
firstPoint()
#secondPoint()
#thirdPoint()