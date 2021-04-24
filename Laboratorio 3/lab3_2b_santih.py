import shared
from matplotlib import pyplot
from matplotlib.ticker import EngFormatter as plotTickFormatter

POINT_TITLE = "Punto 2b"

EEG_SIGNAL_FILE = "eeg_1min.csv"
EEG_SAMPLING_FREQUENCY = 500

HERTZ = "Hz"
HIGHLIGHT_BAND_COLOR = "gray"

BANDS_FIGURE_TITLE = "Comparison of Transformed EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed on a limit of {}Hz"

EEG_BANDS_LIST = [
    (0, 0, "Original Signal", 1),
    (30, 0 , "Gamma", 3),
    (12, 30 , "Beta", 5),
    (8, 12 , "Alpha", 2),
    (4, 7 , "Theta", 4),
    (0, 4 , "Delta", 6)
]

PLOT_LIMIT_FREQUENCY = 65

tick_formatter = plotTickFormatter(unit=HERTZ, sep="")
noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)

def splitFftBands(eeg_bands_list, eeg_signal, start_unfiltered=True):
    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(PLOT_LIMIT_FREQUENCY))
    axis = pyplot.subplot(3, 2, 1)
    pyplot.subplots_adjust(bottom=0.07, top=0.93, left=0.05, right=.95,  wspace=0.1, hspace=0.25)

    for band in eeg_bands_list:
        frequency_array, eeg_band = shared.getEegBand(eeg_signal, EEG_SAMPLING_FREQUENCY, band, return_fft=True, do_not_filter=start_unfiltered)
        lower_bound, higher_bound, eeg_band_title, eeg_band_plot_index = band
        
        if higher_bound == 0: higher_bound = 1000

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, yticks=[], ylabel=eeg_band_title)
        axis.xaxis.set_major_formatter(tick_formatter)
        axis.set_xlim(0, PLOT_LIMIT_FREQUENCY)
        pyplot.axvspan(lower_bound, higher_bound, facecolor=HIGHLIGHT_BAND_COLOR, alpha=0.5)
        pyplot.plot(frequency_array, eeg_band)

        start_unfiltered = False
    
    pyplot.show()

shared.clear(POINT_TITLE)
splitFftBands(EEG_BANDS_LIST, noisy_eeg_signal)