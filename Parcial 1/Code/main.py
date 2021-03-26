import pandas
import os
import platform
import matplotlib.pyplot as plt
import numpy as np

NEURAL_DATA_CSV_LOCATION = "../neural_data.csv"
ECG_CSV_LOCATION = "../ecg.csv"
NEURAL_DATA_CSV_KEY_1 = "Neuron 1"
NEURAL_DATA_CSV_KEY_2 = "Neuron 2"
ECG_CSV_KEY = "ECG"

if not ("/Parcial 1/Code" in os.getcwd()):
    os.chdir(os.getcwd() + "/Parcial 1/Code")

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def printResponse(response):
    clear()
    print(response)

def firstPoint():
    sampling_period = 0.0002

    neural_data_csv = pandas.read_csv(NEURAL_DATA_CSV_LOCATION)
    neural_data_1_array = neural_data_csv[NEURAL_DATA_CSV_KEY_1]
    neural_data_2_array = neural_data_csv[NEURAL_DATA_CSV_KEY_2]
    time_array = np.arange(len(neural_data_1_array))

    def moveSignal(signal_array, number):
        for i in range(65):    
            first = signal_array[0];    
            
            for j in range(len(signal_array) - 1):    
                signal_array[j] = signal_array[j+1];    
                
        signal_array[len(signal_array)-1] = first;    

        return signal_array

    def showSignals():
        figure = plt.figure("Punto 1")
        figure.suptitle("Señales Neuronales")
        plt.xlabel("Tiempo (s)")
        plt.xlabel("x(t)")
        plt.plot(time_array, neural_data_1_array)
        plt.plot(time_array, neural_data_2_array, color="orange")
        plt.show()

    def correlate():
        npts = len(neural_data_1_array)
        x = np.linspace(0, 50, npts)

        lags = np.arange(-npts + 1, npts)
        ccov = np.correlate(neural_data_1_array - neural_data_1_array.mean(), neural_data_2_array - neural_data_2_array.mean(), mode='full')
        ccor = ccov / ((npts - 1) * neural_data_1_array.std() * neural_data_2_array.std())

        fig, axs = plt.subplots(nrows=2)
        fig.subplots_adjust(hspace=0.4)
        

        ax = axs[0]
        ax.plot(lags, ccor)
        #ax.set_ylim(-1, 1)
        ax.set_ylabel('cross-correlation')
        ax.set_xlabel('lag of neural_data_1_array relative to neural_data_2_array')



        maxlag = lags[np.argmax(ccor)]
        
        print("Moviendo grafica, por favor espere...")
        neural_data_2_array_moved = moveSignal(neural_data_2_array, abs(maxlag))

        ax = axs[1]
        ax.plot(x, neural_data_1_array, 'b', label='neural data 1')
        ax.plot(x, neural_data_2_array_moved, 'r', label='neural data 2 (moved)')
        #ax.set_ylim(-10, 10)
        ax.legend(loc='upper right', fontsize='small', ncol=2)

        response = ("Las dos señales producidas por las neuronas son muy similares y al "
                    "mover la segunda señal al punto con mayor correlación vemos que son "
                    "casi identicas, por esto en mi opinion las dos neuronas SI estan "
                    "asociadas en su funcion")
                    
        print("La correlacion maxima esta en: {}\n".format(maxlag))
        printResponse(response)

        plt.show()

    showSignals()
    correlate()

def secondPoint():
    ecg_csv = pandas.read_csv(ECG_CSV_LOCATION)
    ecg_array = ecg_csv[ECG_CSV_KEY]
    sampling_frequency = 1000
    number_of_samples = len (ecg_array)
    sampling_divider = sampling_frequency / 2.5
    zoomed_number_of_samples = int(number_of_samples // sampling_divider)
    time_array = np.arange(len(ecg_array))

    def showFrequencySpectrum(signal_array, number_of_samples, zoomed_number_of_samples):
        transformed_signal_array = np.abs(np.fft.fft(signal_array))
        transformed_signal_array = transformed_signal_array[: number_of_samples // 2]
        zoomed_signal_array = transformed_signal_array[:zoomed_number_of_samples]
        frequency_array = (sampling_frequency)*(np.arange(number_of_samples) / number_of_samples)
        zoomed_frequency_array = (sampling_frequency / sampling_divider)*(np.arange(zoomed_number_of_samples) / zoomed_number_of_samples)

        plt.figure("Punto 2a")
        plt.plot(zoomed_frequency_array, zoomed_signal_array)
        plt.title("Espectro de Frecuencia")
        plt.xlabel("Frecuencia (Hz)")

        response = ("Al graficar el espectro de frecuencia y hacer zoom en el area de "
                        "0 a 2.5Hz, vemos que hay un pico en {}Hz, y por eso esta es la frecuencia "
                        "de nuestro ruido")

        arg_max_signal = np.argmax(signal_array)
        noise_frequency = zoomed_frequency_array[np.argmax(zoomed_signal_array)]

        printResponse(response.format(noise_frequency))
        plt.show()

        return frequency_array, transformed_signal_array, noise_frequency, arg_max_signal
    
    def applyFourierTransform(signal_array, number_of_components, number_of_samples):
        array = np.fft.fft(signal_array)
        blank_index = np.arange(number_of_components, number_of_samples - (number_of_components - 1))
        array[blank_index] = 0 + 0j

        return array

    def ifftReconstruct(signal_array, number_of_components, number_of_samples):
        #transformed_signal = applyFourierTransform(signal_array, number_of_components, number_of_samples)
        reconstructed_signal = np.fft.ifft(signal_array)

        return np.real(reconstructed_signal)

    def plotSignal(time_array, signal_array):
        plt.figure("Punto 2b")
        plt.plot(time_array, signal_array)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("x(t)")
        plt.show()

    ecg_frequency_array, ecg_signal_array, noise_frequency, arg_max_signal = showFrequencySpectrum(ecg_array, number_of_samples, zoomed_number_of_samples)
    #transformed_ecg_array = applyFourierTransform(ecg_array, noise_frequency, number_of_samples)
    #index_to_remove = ecg_frequency_array[]
    #mi_ecg = ecg_signal_array[arg_max_signal: (len(ecg_signal_array) - arg_max_signal)]
    #reconstructed_ecg = ifftReconstruct(mi_ecg, 1024, number_of_samples)
    #plotSignal(time_array, reconstructed_ecg)

clear()
firstPoint()
secondPoint()