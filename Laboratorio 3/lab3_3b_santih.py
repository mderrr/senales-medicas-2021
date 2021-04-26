import shared
import numpy
from matplotlib import pyplot
from scipy import signal
from lab3_3a_santih import showEcgComparison

POINT_TITLE = "Punto 3a"
NEWBORN_SIGNAL_FILE = "apnea.csv"

NEWBORN_CSV_KEYS = ["Neonato 1", "Neonato 2"]




def calculateHeartRate(signal_array, signal_sampling_frequency):
    #filtered_ecg_signal = showEcgComparison(signal_array, signal_sampling_frequency, 1)
    filtered_ecg_signal = shared.filterSignal(signal_array, signal_sampling_frequency, 0.5, 20, acount_for_dc_level=True)



    relative_maximums_array = signal.argrelmax(filtered_ecg_signal)[0] # Gives the argument of a relative max
    #print(relative_maximums_array)

    lista_a =[]

    rms = shared.getRootMeanSquare(filtered_ecg_signal)

    cosa = numpy.max(filtered_ecg_signal) - numpy.max(filtered_ecg_signal) / 10#1.15#1.11

    listra_avg=[cosa] * len(filtered_ecg_signal)

    #listra_avg=[rms] * len(filtered_ecg_signal)

    
    print("MAX", numpy.max(filtered_ecg_signal))
    print("COSA", cosa)

    for argument in relative_maximums_array:
        #value_of_relative_maximum = filtered_ecg_signal.index(argument)
        #print(argument)
        #print("AAAAAAAAAAAAAAAAAAAAA", filtered_ecg_signal[argument])

        if filtered_ecg_signal[argument] > cosa:
            print(argument)
            lista_a.append(argument)

        #if (filtered_ecg_signal[sig[b[i]]])

    '''for i in range(len(relative_maximums_array)):
        sig[b[i]]

        if sig[b[i]] > cosa: #0.2: 
            print(b[i])
            lista_a.append(b[i])'''

    pyplot.figure()

    for i in lista_a:
        pyplot.axvline(x=i, color=shared.COLOR_RED, alpha=0.8, linestyle=shared.LINESTYLE_DASHED)
    
    pyplot.plot(listra_avg)
    pyplot.xlim(0, 1000)
    pyplot.plot(filtered_ecg_signal)

    def getIntantHeartRate(peaks_array, sampling_frequency):
        sampling_period = 1 / sampling_frequency
        instant_heart_rate_array=[]

        for i in range(len(peaks_array)):
            try:
                peak_difference = peaks_array[i] - peaks_array[i - 1]
            except KeyError:
                peak_difference = peaks_array[i]

            peak_period = peak_difference * sampling_period
            instant_heart_rate = (1 / peak_period) * 60

            instant_heart_rate_array.append(instant_heart_rate)

        print(instant_heart_rate_array)
        print("AAAAAAA", round(numpy.mean(instant_heart_rate_array)))



    print("heart_rate", len(lista_a))

    getIntantHeartRate(lista_a, signal_sampling_frequency)

    pyplot.show()




@shared.presentPoint
def main():
    noisy_first_newborn_signal = shared.getSignalFromFile(NEWBORN_SIGNAL_FILE, NEWBORN_CSV_KEYS[0])
    noisy_second_newborn_signal = shared.getSignalFromFile(NEWBORN_SIGNAL_FILE, NEWBORN_CSV_KEYS[1])
    newborn_signal_sampling_rate = int(len(noisy_first_newborn_signal) / 60)

    calculateHeartRate(noisy_second_newborn_signal, newborn_signal_sampling_rate)

if __name__ == "__main__":
    main()