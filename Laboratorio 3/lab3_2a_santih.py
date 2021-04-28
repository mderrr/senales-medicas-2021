import random
import shared
from matplotlib import pyplot

RMS_FORMAT = "RMS of {}"
BANDS_FIGURE_TITLE = "Comparison of EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed in a window of {}s"

ZOOM_IN_SECONDS = 6

def splitEegBands(signal_array, signal_sampling_frequency, eeg_bands_list, start_unfiltered=True, display_rms=False, zoom_in_seconds=None):
    zoom_in_seconds = zoom_in_seconds if zoom_in_seconds is not None else ZOOM_IN_SECONDS

    rms_values_dictionary = {}
    time_range = signal_sampling_frequency * zoom_in_seconds
    start_index = random.randint(0, (len(signal_array) - time_range))
    
    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(zoom_in_seconds), size=shared.SUPTITLE_FONT_SIZE)
    pyplot.subplots_adjust(bottom=0.025, top=0.85, left=0.025, right=.975, wspace=0.05, hspace=0.25)
    axis = pyplot.subplot(3, 2, 1)

    for eeg_band_data in eeg_bands_list:
        _, _, eeg_band_title, eeg_band_plot_index, eeg_line_color = eeg_band_data
        eeg_band = shared.getEegBand(signal_array, signal_sampling_frequency, eeg_band_data, do_not_filter=start_unfiltered)

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, xticks=[], yticks=[])
        axis.set_title(eeg_band_title, size=shared.LABEL_FONT_SIZE)
        axis.set_xlim(start_index, start_index + time_range)
        pyplot.plot(eeg_band, color=eeg_line_color)

        if display_rms:
            rms_value = shared.getRootMeanSquare(eeg_band)
            rms_line = [rms_value] * len(eeg_band)

            rms_values_dictionary[eeg_band_title] = rms_value

            pyplot.plot(rms_line, label=RMS_FORMAT.format(round(rms_value)), color=shared.COLOR_RED)
            pyplot.legend()

        start_unfiltered = False
    
    pyplot.show()
    return list(rms_values_dictionary.items())

@shared.presentPoint
def main():
    noisy_eeg_signal = shared.getSignalFromFile(shared.EEG_FILE_NAME)

    splitEegBands(noisy_eeg_signal, shared.EEG_SAMPLING_FREQUENCY, shared.getEegBandsList(verbose=True))

if __name__ == "__main__":
    main()