import numpy
from matplotlib import pyplot
import lab5_shared_santih as shared

EMG_FILE_PATH          = "./emg_lesion.csv"
DAY_KEY_FORMAT         = "DIA {}"
FIGURE_TITLE           = "Resistance"
FIGURE_SUPTITLE        = "Plot of patient's resistance"
X_LABEL                = "Day"
Y_LABEL                = "Resistance time (s)"
DEFAULT_CONVOLVE_MODE  = "same"

DAY_LABELS             = [ "Day 0"
                         , "Day 5"
                         , "Day 15"
                         , "Day 20"
                         , "Day 30"
                         ]

EMG_SAMPLING_FREQUENCY = 1_000
DAYS_ARRAY             = [0, 5, 15, 20, 30]

def getRmsEnvelopedSignal(signal_array, window_size=None, convolve_mode=None):
    window_size          = window_size if window_size is not None else 400 # A size of 400 for the window seems to give best looking and most accurate result
    convolve_mode        = convolve_mode if convolve_mode is not None else DEFAULT_CONVOLVE_MODE

    squared_signal_array = signal_array ** 2
    window_array         = numpy.ones(window_size) / float(window_size) # To make every item 1 / window_size

    return numpy.sqrt(numpy.convolve(squared_signal_array, window_array, convolve_mode))

def calculateInterval(signal_array, signal_sampling_frequency):
    signal_mean           = numpy.mean(signal_array)
    values_over_threshold = [value for value in signal_array if value >= signal_mean]

    return (1 / signal_sampling_frequency) * len(values_over_threshold)
                
@shared.presentPoint
def main():
    emg_signals            = [ shared.getSignalFromFile(EMG_FILE_PATH, DAY_KEY_FORMAT.format(i)) for i in DAYS_ARRAY ]
    enveloped_signals      = [ getRmsEnvelopedSignal(emg_signals[i]) for i in range(len(DAYS_ARRAY)) ]
    calculated_times_array = [ calculateInterval(enveloped_signals[i], EMG_SAMPLING_FREQUENCY) for i in range(len(DAYS_ARRAY)) ]

    pyplot.figure(FIGURE_TITLE)
    pyplot.suptitle(FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.plot(DAYS_ARRAY, calculated_times_array)
    pyplot.plot(DAYS_ARRAY, calculated_times_array, shared.BLUE_OBJECT)
    pyplot.xlabel(X_LABEL)
    pyplot.ylabel(Y_LABEL)
    pyplot.show()

if __name__ == "__main__":
    main()