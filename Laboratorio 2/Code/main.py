import os
import math
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from statistics import mean

# =========================================================== #
#  IMPORTANTE MANTENER LA ESTRUCTURA DEL CODIGO, EL ARCHIVO   #
#    'main.py' DEBE ESTAR DENTRO DE 'Laboratorio 2/Code'      #
#  O PUEDE SER ABIERTO DIRECTAMENTE DESDE LA CARPETA 'Code'   #
# =========================================================== #
WORKING_DIRECTORY = "/Laboratorio 2/Code"

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
        
INSTANT_HEART_RATE_TITLE = "\nFrecuencias cardiacas instantaneas:"
INSTANT_HEART_RATE_FORMAT = "{} Lpm"
AVERAGE_HEART_RATE_MESSAGE = "Frecuencia cardiaca promedio:"

SIGNAL1_CSV_LOCATION = "../signal1.csv"
ECG_CSV_LOCATION = "../ecg_1min.csv"
ECG_PEAKS_CSV_LOCATION = "../ecg_1min_rpeaks.csv"

SIGNAL1_CSV_KEY = "Signal"
ECG_CSV_KEY = "ECG"
ECG_PEAKS_CSV_KEY = "R peaks"

WINDOWS_PLATFORM_NAME = "Windows"
WINDOWS_CLEAR = "cls"
UNIX_CLEAR = "clear"
SPACE = " "
COMMA = ", "
COMMA_ELLIPSIS = COMMA + "..."
CENTER = "center"
VERTICAL = "vertical"
ENABLED = "Enabled"
DISABLED = "Disabled"
DASHED = "dashed"
C, B = ("c", "b")

GENERATED_SIGNAL, RECONSTRUCTED_SIGNAL, ORIGINAL_CSV_SIGNAL, PORTIONED_CSV_SIGNAL, ECG_CSV_SIGNAL = ("A", "B", "C", "D", "E")
X, Y = ("X", "Y")
WINDOW_TITLE, SUPTITLE, PLOT_TITLES, X_LABELS, Y_LABELS = ("WINDOW_TITLE", "SUPTITLE", "PLOT_TITLES", "X_LABELS", "Y_LABELS")

SUBPLOT_INFO = {
    GENERATED_SIGNAL: {
        X: 1,
        Y: 2,
        WINDOW_TITLE: "Punto 1)",
        SUPTITLE: "Sawtooth Signal",
        PLOT_TITLES: ["Signal", "Frequency Spectrum"],
        X_LABELS: ["Time (s)", "Frequency (Hz)"]
    },
    RECONSTRUCTED_SIGNAL: {
        X: 1,
        Y: 2,
        WINDOW_TITLE: "Punto 1)",
        SUPTITLE: "{} Point Signal Reconstruction",
        PLOT_TITLES: ["Using IFFT", "Using Ecuation"],
        X_LABELS: ["Time (s)"],
        Y_LABELS: ["x(t)"]
    },
    ORIGINAL_CSV_SIGNAL: {
        X: 2,
        Y: 3,
        WINDOW_TITLE: "Punto 2a)",
        SUPTITLE: "Complete Frequency Spectrum",
        X_LABELS: ["Frequency (Hz)"]
    },
    PORTIONED_CSV_SIGNAL: {
        X: 2,
        Y: 3,
        WINDOW_TITLE: "Punto 2{})",
        SUPTITLE: "Portioned Frequency Spectrums With Zero Padding {}",
        PLOT_TITLES: ["From 1 to {}"],
    },
    ECG_CSV_SIGNAL: {
        X: 1,
        Y: 2,
        WINDOW_TITLE: "Punto 3a)",
        SUPTITLE: "ECG Frequency Spectrums",
        PLOT_TITLES: ["Complete Frequency", "Zoomed In Frequency"],
    }
}

FIRST_POINT, SECOND_POINT, THIRD_POINT = (0, 1, 2)

SAMPLING_FREQUENCIES = [1024, 1000, 250]
TOTAL_TIMES = [1]

ECG_FREQUENCY_CUTTING_POINT = 20

RECONSTRUCTION_COMPONENTS = 24

if not (WORKING_DIRECTORY in os.getcwd()):
    os.chdir(os.getcwd() + WORKING_DIRECTORY)

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

        signal_array[: number_of_samples // 2] = time_array[: number_of_samples // 2]
        signal_array[number_of_samples // 2 : number_of_samples] = time_array[: number_of_samples // 2]

        # Signal transforms to match example
        signal_array *= 2
        signal_array -= .5

        transformed_signal_array = np.abs(np.fft.fft(signal_array))
        transformed_signal_array = transformed_signal_array[: number_of_samples // 2]
        frequency_array = (sampling_frequency // 2) * (np.arange(number_of_samples // 2) / (number_of_samples // 2))

        figure, (subplot_original, subplot_transformed) = plt.subplots(SUBPLOT_INFO[GENERATED_SIGNAL][X], SUBPLOT_INFO[GENERATED_SIGNAL][Y], num=SUBPLOT_INFO[GENERATED_SIGNAL][WINDOW_TITLE])
        figure.suptitle(SUBPLOT_INFO[GENERATED_SIGNAL][SUPTITLE])
        subplot_original.plot(time_array, signal_array)
        subplot_original.set_title(SUBPLOT_INFO[GENERATED_SIGNAL][PLOT_TITLES][0])
        subplot_original.set_xlabel(SUBPLOT_INFO[GENERATED_SIGNAL][X_LABELS][0])
        subplot_transformed.plot(frequency_array, transformed_signal_array)
        subplot_transformed.set_title(SUBPLOT_INFO[GENERATED_SIGNAL][PLOT_TITLES][1])
        subplot_transformed.set_xlabel(SUBPLOT_INFO[GENERATED_SIGNAL][X_LABELS][1])
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

    def plotReconstructedSignals(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array, number_of_components):
        figure, (subplot_ifft, subplot_ecuation) = plt.subplots(SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][X], SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][Y], num=SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][WINDOW_TITLE])
        figure.suptitle(SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][SUPTITLE].format(number_of_components))
        figure.text(0.5, 0.04, SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][X_LABELS][0], ha=CENTER)
        figure.text(0.04, 0.5, SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][Y_LABELS][0], va=CENTER, rotation=VERTICAL)
        subplot_ifft.plot(time_array, ifft_reconstructed_signal)
        subplot_ifft.plot(time_array, base_signal_array, linestyle=DASHED)
        subplot_ifft.set_title(SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][PLOT_TITLES][0])
        subplot_ecuation.plot(time_array, ecuation_reconstructed_signal)
        subplot_ecuation.plot(time_array, base_signal_array, linestyle=DASHED)
        subplot_ecuation.set_title(SUBPLOT_INFO[RECONSTRUCTED_SIGNAL][PLOT_TITLES][1])
        plt.show()

    time_array, base_signal_array = generateSignal(sampling_frequency, total_time, number_of_samples)
    ifft_reconstructed_signal = ifftReconstruct(base_signal_array, RECONSTRUCTION_COMPONENTS, number_of_samples)
    ecuation_reconstructed_signal = ecuationReconstruct(number_of_samples, RECONSTRUCTION_COMPONENTS, base_frequency, base_signal_array, time_array)
    plotReconstructedSignals(time_array, ifft_reconstructed_signal, ecuation_reconstructed_signal, base_signal_array, RECONSTRUCTION_COMPONENTS)

def secondPoint():
    signal1_csv = pd.read_csv(SIGNAL1_CSV_LOCATION)
    signal_array = signal1_csv[SIGNAL1_CSV_KEY]
    sampling_frequency = SAMPLING_FREQUENCIES[SECOND_POINT]    
    number_of_samples = len(signal_array)

    transformed_signal = np.abs(np.fft.fft(signal_array))
    transformed_signal = transformed_signal[:number_of_samples // 2]
    base_frequency = (sampling_frequency // 2) * (np.arange(number_of_samples // 2) / (number_of_samples // 2))

    def displayOriginal():
        plt.figure(SUBPLOT_INFO[ORIGINAL_CSV_SIGNAL][WINDOW_TITLE])
        plt.title(SUBPLOT_INFO[ORIGINAL_CSV_SIGNAL][SUPTITLE])
        plt.xlabel(SUBPLOT_INFO[ORIGINAL_CSV_SIGNAL][X_LABELS][0])
        plt.plot(base_frequency, transformed_signal)
        plt.show()

    def displayPortionedFrequencies(zero_padding=False):
        figure, plots = plt.subplots(SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][X], SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][Y], num=SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][WINDOW_TITLE].format(C if zero_padding else B))

        for x in range(SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][X]):
            for y in range(SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][Y]):
                current_plot = plots[x, y]
                one_dimensional_index = (x * SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][Y]) + y
                frequency_divider = 1 * pow(2, one_dimensional_index)
                relative_number_of_samples = number_of_samples // frequency_divider
                relative_signal = np.zeros((number_of_samples) if zero_padding else relative_number_of_samples)
                relative_signal[:relative_number_of_samples] = signal_array[:relative_number_of_samples]  
                transformed_relative_signal = np.abs(np.fft.fft(relative_signal))

                if zero_padding:
                    relative_frequency = base_frequency
                    transformed_relative_signal = transformed_relative_signal[:number_of_samples // 2]
                else:
                    relative_frequency = (sampling_frequency // 2) * (np.arange(relative_number_of_samples // 2) / (relative_number_of_samples // 2))
                    transformed_relative_signal = transformed_relative_signal[:relative_number_of_samples // 2]

                current_plot.plot(relative_frequency, transformed_relative_signal)
                current_plot.set_title(SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][PLOT_TITLES][0].format(relative_number_of_samples))

        figure.suptitle(SUBPLOT_INFO[PORTIONED_CSV_SIGNAL][SUPTITLE].format(ENABLED if zero_padding else DISABLED))
        plt.show()

    displayOriginal()

    printResponse(POINT_2B_RESPONSE)
    displayPortionedFrequencies()
   
    printResponse(POINT_2C_RESPONSE)
    displayPortionedFrequencies(True)
    
def thirdPoint():
    ecg_csv = pd.read_csv(ECG_CSV_LOCATION)
    ecg_peaks_csv = pd.read_csv(ECG_PEAKS_CSV_LOCATION)
    ecg_array = ecg_csv[ECG_CSV_KEY]
    ecg_peaks_array = ecg_peaks_csv[ECG_PEAKS_CSV_KEY]
    sampling_frequency = SAMPLING_FREQUENCIES[THIRD_POINT]
    sampling_divider = sampling_frequency / ECG_FREQUENCY_CUTTING_POINT
    number_of_samples = len(ecg_array)
    zoomed_number_of_samples = int(number_of_samples // sampling_divider)

    def displayFrequencies():
        transformed_ecg_array = np.abs(np.fft.fft(ecg_array))
        half_transformed_ecg_array = transformed_ecg_array[:number_of_samples // 2]
        zoomed_ecg_array = transformed_ecg_array[:zoomed_number_of_samples]
        frequency_array = (sampling_frequency) * (np.arange(number_of_samples) / number_of_samples)
        half_frequency_array = (sampling_frequency / 2) * (np.arange(number_of_samples / 2) / number_of_samples / 2)
        zoomed_frequency_array = (sampling_frequency / sampling_divider)*(np.arange(zoomed_number_of_samples) / zoomed_number_of_samples)

        figure, (subplot_original, subplot_zoomed) = plt.subplots(SUBPLOT_INFO[ECG_CSV_SIGNAL][X], SUBPLOT_INFO[ECG_CSV_SIGNAL][Y], num=SUBPLOT_INFO[ECG_CSV_SIGNAL][WINDOW_TITLE])
        figure.suptitle(SUBPLOT_INFO[ECG_CSV_SIGNAL][SUPTITLE])
        subplot_original.plot(half_frequency_array, half_transformed_ecg_array)
        subplot_original.set_title(SUBPLOT_INFO[ECG_CSV_SIGNAL][PLOT_TITLES][0])
        subplot_zoomed.plot(zoomed_frequency_array, zoomed_ecg_array)
        subplot_zoomed.set_title(SUBPLOT_INFO[ECG_CSV_SIGNAL][PLOT_TITLES][1])

        # Heart Rate
        max_frecuency_position = np.argmax(transformed_ecg_array)
        max_frecuency_value = frequency_array[max_frecuency_position]
        heart_rate = max_frecuency_value * 60

        printResponse(POINT_3A_RESPONSE.format(max_frecuency_position, round(max_frecuency_value, 2), round(heart_rate)))
        plt.show()

    def getIntantHeartRate():
        sampling_period = 1 / sampling_frequency
        instant_heart_rate_array=[]

        for i in range(len(ecg_peaks_array)):
            try:
                peak_difference = ecg_peaks_array[i] - ecg_peaks_array[i - 1]
            except KeyError:
                peak_difference = ecg_peaks_array[i]

            peak_period = peak_difference * sampling_period
            instant_heart_rate = (1 / peak_period) * 60

            instant_heart_rate_array.append(instant_heart_rate)

        printResponse(POINT_3B_RESPONSE)
        printShortList(instant_heart_rate_array, INSTANT_HEART_RATE_TITLE, INSTANT_HEART_RATE_FORMAT)
        print(AVERAGE_HEART_RATE_MESSAGE, round(mean(instant_heart_rate_array)))
        
    displayFrequencies()
    getIntantHeartRate()

clear()
firstPoint()
secondPoint()
thirdPoint()