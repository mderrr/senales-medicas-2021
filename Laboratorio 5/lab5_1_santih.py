import numpy
import pandas
from scipy import signal
from matplotlib import pyplot

from lab5_shared_santih import getSignalFromFile

def removeSignalOutliers(signal_list: list[float], standard_deviation_multiplier: int = None) -> list[float]:
    filtered_signal_list: list[float]

    standard_deviation_multiplier = 10 if standard_deviation_multiplier is None else standard_deviation_multiplier

    filtered_signal_list = numpy.where( signal_list > ( numpy.mean(signal_list) + standard_deviation_multiplier * numpy.std(signal_list) ), numpy.mean(signal_list), signal_list )
    filtered_signal_list = numpy.where( signal_list < ( numpy.mean(signal_list) - standard_deviation_multiplier * numpy.std(signal_list) ), numpy.mean(signal_list), signal_list )

    return filtered_signal_list

def filterAbpSignal(abp_signal_list, abp_sampling_frequency):
    filter_order = 3
    filter_type  = "lowpass"

    wn = 15 / (abp_sampling_frequency / 2)
    b, a = signal.butter(filter_order, wn, filter_type)
    filtered_abp_list = signal.filtfilt(b, a, abp_signal_list)

    return filtered_abp_list

def getAbpPeaks(abp_list, abp_sampling_frequency):
    thres = 0.55

    modified_abp_list = removeSignalOutliers(abp_list)
    modified_abp_list = filterAbpSignal(modified_abp_list, abp_sampling_frequency)

    # Algoritmo
    aux = numpy.abs( numpy.diff(modified_abp_list) )
    n = int( numpy.round(fs / 5) )
    aux2 = numpy.zeros( len(aux) )

    for i in range(n, len(aux)): # integral móvil con ventana n
        aux2[i] = numpy.sum(aux[i - n:i])

    aux2_thres = numpy.max(aux2)
    aux3 = ( aux2 > (thres * aux2_thres) ) * 1
    aux4 = numpy.diff(aux3)
    l_izq = numpy.where(aux4 == 1)
    l_der = numpy.where(aux4 == -1)
    l_izq = l_izq - numpy.array(n / 2)

    # Peaks
    maximum_peaks = numpy.ones( numpy.size(l_izq) - 1 )
    minimum_peaks = numpy.ones( numpy.size(l_izq) - 1 )

    for i in range(0, numpy.size(l_izq) - 1):
        ind_max = numpy.argmax( modified_abp_list[int(l_izq[0][i]):int(l_der[0][i])] )
        ind_min = numpy.argmin( modified_abp_list[int(l_izq[0][i]):int(l_der[0][i])] )

        maximum_peaks[i] = ind_max + l_izq[0][i]
        minimum_peaks[i] = ind_min + l_izq[0][i]

    # Peaks as Ints
    ind_maximum_peaks = [0 for i in range(len(maximum_peaks))]
    ind_minimum_peaks = [0 for i in range(len(minimum_peaks))]

    for i in range(len(maximum_peaks)):
        ind_maximum_peaks[i] = int(maximum_peaks[i])
        ind_minimum_peaks[i] = int(minimum_peaks[i])

    pressure_variance = [modified_abp_list[ind_maximum_peaks[i]] - modified_abp_list[ind_minimum_peaks[i]] for i in range(len(ind_maximum_peaks))]

    return ind_maximum_peaks, ind_minimum_peaks, pressure_variance

abp_signal = getSignalFromFile("./abp2.csv")
fs = 125

maximum_peaks_indices, minimum_peaks_indices, pressure_variance = getAbpPeaks(abp_signal, fs)

pyplot.plot(abp_signal)
pyplot.plot(maximum_peaks_indices, abp_signal[maximum_peaks_indices], "ro", label="Peaks")
pyplot.plot(minimum_peaks_indices, abp_signal[minimum_peaks_indices], "go", label="Valleys")
pyplot.plot(maximum_peaks_indices, pressure_variance, label="Pressure Variance")
pyplot.legend()
pyplot.show()