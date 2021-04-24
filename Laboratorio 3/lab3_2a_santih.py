import shared
from scipy import signal
from matplotlib import pyplot
import numpy
import random

POINT_TITLE = "Punto 2a"

EEG_SIGNAL_FILE = "eeg_1min.csv"
EEG_SAMPLING_FREQUENCY = 500

BANDS_FIGURE_TITLE = "Comparison of EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed in a window of {}s"
ORIGINAL_SIGNAL_TITLE = "Original Signal"

EEG_BANDS_LIST = [
    (30, 0 , "Gamma - 30Hz to 100Hz+", 3),
    (12, 30 , "Beta - 12Hz to 30Hz", 5),
    (8, 12 , "Alpha - 8Hz to 12Hz", 2),
    (4, 7 , "Theta - 4Hz to 7Hz", 4),
    (0, 4 , "Delta - 0Hz to 4Hz", 6)
]

noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)

def getEegBand(noisy_signal, signal_sampling_rate, band_bounds):
    filter_type = shared.BANDPASS
    lower_bound, higher_bound, _, _ = band_bounds
    low_cutoff = lower_bound / (signal_sampling_rate / 2)
    high_cutoff = higher_bound / (signal_sampling_rate / 2)

    if (lower_bound < 1):
        cutoff_frequencies = high_cutoff
        filter_type = shared.LOWPASS

    elif (higher_bound == 0):
        cutoff_frequencies = low_cutoff
        filter_type = shared.HIGHPASS

    else:
        cutoff_frequencies = [low_cutoff, high_cutoff]

    b, a = signal.butter(4, cutoff_frequencies, filter_type)
    filtered_signal = signal.filtfilt(b, a, noisy_signal) 

    return filtered_signal

def splitEegBands(eeg_bands_list, eeg_signal):
    time_range = (EEG_SAMPLING_FREQUENCY * 6) # / 6
    time_period = round(time_range * (1 / EEG_SAMPLING_FREQUENCY))
    start_index = random.randint(0, (len(noisy_eeg_signal) - time_range))

    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(time_period))
    axis = pyplot.subplot(3, 2, 1, xticks=[], yticks=[], title=ORIGINAL_SIGNAL_TITLE)
    pyplot.plot(eeg_signal)

    for band in eeg_bands_list:
        eeg_band = getEegBand(noisy_eeg_signal, EEG_SAMPLING_FREQUENCY, band)
        _, _, eeg_band_title, eeg_band_plot_index = band

        pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, xticks=[], yticks=[], title=eeg_band_title)
        pyplot.plot(eeg_band)

    pyplot.xlim(start_index, start_index + time_range)
    pyplot.subplots_adjust(bottom=0.025, left=0.025, right=.975, wspace=0.05, hspace=0.25)
    pyplot.show()

shared.clear(POINT_TITLE)
splitEegBands(EEG_BANDS_LIST, noisy_eeg_signal)