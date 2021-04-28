import shared
from matplotlib import pyplot

BANDS_FIGURE_TITLE = "Comparison of Transformed EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed on a limit of {}Hz"

PLOT_LIMIT_FREQUENCY = 60

def splitFftBands(eeg_signal, eeg_signal_sampling_frequency, eeg_bands_list, plot_frequency_limit=None, start_unfiltered=True):
    tick_formatter = shared.getPlotTickFormatter(shared.UNIT_HERTZ)
    plot_frequency_limit = plot_frequency_limit if plot_frequency_limit is not None else PLOT_LIMIT_FREQUENCY

    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(plot_frequency_limit), size=shared.SUPTITLE_FONT_SIZE)
    axis = pyplot.subplot(3, 2, 1)
    pyplot.subplots_adjust(bottom=0.07, top=0.92, left=0.05, right=.95,  wspace=0.1, hspace=0.25)

    for band_data in eeg_bands_list:
        frequency_array, eeg_band_array = shared.getEegBand(eeg_signal, eeg_signal_sampling_frequency, band_data, return_fft=True, do_not_filter=start_unfiltered)
        lower_bound, higher_bound, eeg_band_title, eeg_band_plot_index, eeg_line_color = band_data
        
        if higher_bound == 0: higher_bound = 1000

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, yticks=[], ylabel=eeg_band_title)
        axis.xaxis.set_major_formatter(tick_formatter)
        axis.set_xlim(0, plot_frequency_limit)
        pyplot.axvspan(lower_bound, higher_bound, facecolor=shared.COLOR_GRAY, alpha=0.5)
        
        pyplot.plot(frequency_array, eeg_band_array, color=eeg_line_color)

        start_unfiltered = False

    pyplot.show()

@shared.presentPoint
def main():
    noisy_eeg_signal = shared.getSignalFromFile(shared.EEG_FILE_NAME)

    splitFftBands(noisy_eeg_signal, shared.EEG_SAMPLING_FREQUENCY, shared.getEegBandsList())

if __name__ == "__main__":
    main()