import shared
from matplotlib import pyplot

EEG_SIGNAL_FILE = "eeg_1min.csv"
EEG_SAMPLING_FREQUENCY = 500

BANDS_FIGURE_TITLE = "Comparison of Transformed EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed on a limit of {}Hz"

PLOT_LIMIT_FREQUENCY = 65

def splitFftBands(eeg_bands_list, eeg_signal, start_unfiltered=True):
    list_of_signals = []
    tick_formatter = shared.getPlotTickFormatter(shared.HERTZ)
    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(PLOT_LIMIT_FREQUENCY), size=shared.SUPTITLE_FONT_SIZE)
    axis = pyplot.subplot(3, 2, 1)
    pyplot.subplots_adjust(bottom=0.07, top=0.92, left=0.05, right=.95,  wspace=0.1, hspace=0.25)

    for band in eeg_bands_list:
        frequency_array, eeg_band = shared.getEegBand(eeg_signal, EEG_SAMPLING_FREQUENCY, band, return_fft=True, do_not_filter=start_unfiltered)
        lower_bound, higher_bound, eeg_band_title, eeg_band_plot_index, eeg_line_color = band
        list_of_signals.append(eeg_band)
        
        if higher_bound == 0: higher_bound = 1000

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, yticks=[], ylabel=eeg_band_title)
        axis.xaxis.set_major_formatter(tick_formatter)
        axis.set_xlim(0, PLOT_LIMIT_FREQUENCY)
        pyplot.axvspan(lower_bound, higher_bound, facecolor=shared.COLOR_GRAY, alpha=0.5)
        pyplot.plot(frequency_array, eeg_band, color=eeg_line_color)

        start_unfiltered = False

    pyplot.show()

@shared.presentPoint
def main():
    noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)
    splitFftBands(shared.getEegBandsList(), noisy_eeg_signal)

if __name__ == "__main__":
    main()