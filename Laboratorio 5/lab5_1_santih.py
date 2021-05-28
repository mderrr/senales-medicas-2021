import numpy
import pandas
from scipy import signal
from matplotlib import pyplot
import lab5_shared_santih as shared

ABP_FILE_PATH            = "./abp1.csv"
PEAKS_FIGURE_TITLE       = "Peaks and Valleys"
PRESSURE_FIGURE_TITLE    = "Pressure Variance"
PRESSURE_FIGURE_SUPTITLE = "Plot of pressure variance"
PEAKS_FIGURE_SUPTITLE    = "Identified peaks and valleys"
PEAK_LABEL               = "Peak"
VALLEY_LABEL             = "Valley"

ABP_SAMPLING_FREQUENCY = 125

def removeSignalOutliers(signal_list, standard_deviation_multiplier = None):
    standard_deviation_multiplier = 10 if standard_deviation_multiplier is None else standard_deviation_multiplier

    filtered_signal_list = numpy.where( signal_list > ( numpy.mean(signal_list) + standard_deviation_multiplier * numpy.std(signal_list) ), numpy.mean(signal_list), signal_list )
    filtered_signal_list = numpy.where( signal_list < ( numpy.mean(signal_list) - standard_deviation_multiplier * numpy.std(signal_list) ), numpy.mean(signal_list), signal_list )

    return filtered_signal_list

def filterAbpSignal(abp_signal_list, abp_sampling_frequency, filter_type = "lowpass", filter_order = 3):
    wn                = 15 / (abp_sampling_frequency / 2)
    b, a              = signal.butter(filter_order, wn, filter_type)
    filtered_abp_list = signal.filtfilt(b, a, abp_signal_list)

    return filtered_abp_list

def getAbpPeaks(abp_list, abp_sampling_frequency):
    thres             = 0.55

    modified_abp_list = removeSignalOutliers(abp_list)
    modified_abp_list = filterAbpSignal(modified_abp_list, abp_sampling_frequency)

    # Algoritmo
    aux               = numpy.abs( numpy.diff(modified_abp_list) )
    n                 = int( numpy.round(abp_sampling_frequency / 5) )
    aux2              = [ numpy.sum(aux[i-n : i]) if i in range(n, len(aux)) else 0 for i in range(len(aux)) ] # integral móvil con ventana n
    aux2_thres        = numpy.max(aux2)
    aux3              = ( aux2 > (thres * aux2_thres) ) * 1
    aux4              = numpy.diff(aux3)
    l_izq             = numpy.where(aux4 == 1)
    l_der             = numpy.where(aux4 == -1)
    l_izq             = l_izq - numpy.array(n / 2)

    # Peaks
    maximum_peaks     = numpy.ones( numpy.size(l_izq) - 1 )
    minimum_peaks     = numpy.ones( numpy.size(l_izq) - 1 )

    for i in range(0, numpy.size(l_izq) - 1):
        ind_max = numpy.argmax( modified_abp_list[int(l_izq[0][i]) : int(l_der[0][i])] )
        ind_min = numpy.argmin( modified_abp_list[int(l_izq[0][i]) : int(l_der[0][i])] )

        maximum_peaks[i] = ind_max + l_izq[0][i]
        minimum_peaks[i] = ind_min + l_izq[0][i]

    # Peaks as Ints
    ind_maximum_peaks = [ int(maximum_peaks[i]) for i in range(len(maximum_peaks)) ]
    ind_minimum_peaks = [ int(minimum_peaks[i]) for i in range(len(minimum_peaks)) ]

    pressure_variance = [ modified_abp_list[ind_maximum_peaks[i]] - modified_abp_list[ind_minimum_peaks[i]] for i in range(len(ind_maximum_peaks)) ]

    return ind_maximum_peaks, ind_minimum_peaks, pressure_variance

@shared.presentPoint
def main():
    abp_signal                                      = shared.getSignalFromFile(ABP_FILE_PATH)
    peak_indices, valley_indices, pressure_variance = getAbpPeaks(abp_signal, ABP_SAMPLING_FREQUENCY)

    # Ploting
    pyplot.figure(PEAKS_FIGURE_TITLE)
    pyplot.suptitle(PEAKS_FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.plot(abp_signal)
    pyplot.plot(peak_indices, abp_signal[peak_indices], shared.RED_OBJECT, label=PEAK_LABEL)
    pyplot.plot(valley_indices, abp_signal[valley_indices], shared.GREEN_OBJECT, label=VALLEY_LABEL)
    pyplot.subplots_adjust(bottom=0.02, top=0.925, left=0.02, right=0.98)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.legend()
    pyplot.show()

    pyplot.figure(PRESSURE_FIGURE_TITLE)
    pyplot.suptitle(PRESSURE_FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.plot(peak_indices, pressure_variance, label=PRESSURE_FIGURE_TITLE)
    pyplot.subplots_adjust(bottom=0.02, top=0.925, left=0.02, right=0.98)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.legend()
    pyplot.show()

if __name__ == "__main__":
    main()