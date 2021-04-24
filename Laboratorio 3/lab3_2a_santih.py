import numpy
import random
import shared
from scipy import signal
from matplotlib import pyplot

POINT_TITLE = "Punto 2a"

EEG_SIGNAL_FILE = "eeg_1min.csv"
EEG_SAMPLING_FREQUENCY = 500

BANDS_FIGURE_TITLE = "Comparison of EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed in a window of {}s"

EEG_BANDS_LIST = [
    (0, 0, "Original Signal", 1),
    (30, 0 , "Gamma - 30Hz to 100Hz+", 3),
    (12, 30 , "Beta - 12Hz to 30Hz", 5),
    (8, 12 , "Alpha - 8Hz to 12Hz", 2),
    (4, 7 , "Theta - 4Hz to 7Hz", 4),
    (0, 4 , "Delta - 0Hz to 4Hz", 6)
]

ZOOM_IN_SECONDS = 6

noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)

def splitEegBands(eeg_bands_list, eeg_signal, display_fft=False, start_unfiltered=True):
    time_range = (EEG_SAMPLING_FREQUENCY * ZOOM_IN_SECONDS) # / 3
    time_period = round(time_range * (1 / EEG_SAMPLING_FREQUENCY))
    start_index = random.randint(0, (len(noisy_eeg_signal) - time_range))

    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(time_period))
    pyplot.subplots_adjust(bottom=0.025, left=0.025, right=.975, wspace=0.05, hspace=0.25)
    axis = pyplot.subplot(3, 2, 1)

    for band in eeg_bands_list:
        _, _, eeg_band_title, eeg_band_plot_index = band
        eeg_band = shared.getEegBand(noisy_eeg_signal, EEG_SAMPLING_FREQUENCY, band, do_not_filter=start_unfiltered)

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, xticks=[], yticks=[], title=eeg_band_title)
        axis.set_xlim(start_index, start_index + time_range)
        pyplot.plot(eeg_band)

        start_unfiltered = False
    
    pyplot.show()

if __name__ == "__main__":
    shared.clear(POINT_TITLE)
    splitEegBands(EEG_BANDS_LIST, noisy_eeg_signal, True)