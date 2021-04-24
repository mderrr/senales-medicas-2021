import shared
from scipy import signal
from matplotlib import pyplot
import numpy

POINT_TITLE = "Punto 1"

ECG_SIGNAL_FILE = "ecg_noisy2.csv"
ECG_SAMPLING_FREQUENCY = 1000

LOW_CUTOFF_VALUE = 0.5
HIGH_CUTOFF_VALUE = 25

FILTERED_FIGURE_TITLE = "Filtered Signal"
FREQUENCY_RESPONSE_FIGURE_TITLE = "Filter Frequency Response"
FILTERED_FIGURE_SUPTITLE = "Filtered with band-pass between {}Hz and {}Hz"

PLOT_LEGEND_TEMPLATE = "{} - {}Hz"

noisy_ecg_signal = shared.getSignalFromFile(ECG_SIGNAL_FILE)

def showSamplingFrequencyTests():
    # Find the best low pass
    shared.testCutoffFrequencies(noisy_ecg_signal, ECG_SAMPLING_FREQUENCY, 0.25, 1.5, 9) # Best looking is ~0.5Hz

    # Find the best high pass
    shared.testCutoffFrequencies(noisy_ecg_signal, ECG_SAMPLING_FREQUENCY, 19, 40, 9, band_to_test=shared.HIGHPASS, stable_cutoff_frequency=0.5) # Best looking is ~25Hz

def applyPassbandFilter():
    low_cutoff = LOW_CUTOFF_VALUE / (ECG_SAMPLING_FREQUENCY / 2)
    high_cutoff = HIGH_CUTOFF_VALUE / (ECG_SAMPLING_FREQUENCY / 2)
    cutoff_frequencies = [low_cutoff, high_cutoff]
    b, a = signal.butter(4, cutoff_frequencies, shared.BANDPASS)
    filtered_ecg_signal = signal.filtfilt(b, a, noisy_ecg_signal) 

    pyplot.figure(FILTERED_FIGURE_TITLE).suptitle(FILTERED_FIGURE_SUPTITLE.format(LOW_CUTOFF_VALUE, HIGH_CUTOFF_VALUE))

    axis = pyplot.subplot(2, 1, 1)
    pyplot.plot(noisy_ecg_signal)

    pyplot.subplot(2, 1, 2, sharex=axis)
    pyplot.plot(filtered_ecg_signal)

    pyplot.show()

def showFilterFrequencyResponse(cutoff_value, sampling_rate, filter_type=shared.LOWPASS, show_plot=False):
    cutoff = cutoff_value / (sampling_rate / 2)
    b, a = signal.butter(4, cutoff, filter_type)
    w, h = signal.freqz(b, a)
    w = (w * sampling_rate) / (2 * numpy.pi)

    pyplot.figure(FREQUENCY_RESPONSE_FIGURE_TITLE)
    pyplot.plot(w, numpy.abs(h), label=PLOT_LEGEND_TEMPLATE.format(filter_type, cutoff_value))
    pyplot.legend()
    pyplot.grid()
    pyplot.xlim(0, 50)
    if show_plot: pyplot.show()

shared.clear(POINT_TITLE)
showSamplingFrequencyTests()
applyPassbandFilter()
showFilterFrequencyResponse(HIGH_CUTOFF_VALUE, ECG_SAMPLING_FREQUENCY)
showFilterFrequencyResponse(LOW_CUTOFF_VALUE, ECG_SAMPLING_FREQUENCY, filter_type=shared.HIGHPASS, show_plot=True)