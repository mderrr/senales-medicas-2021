import random
import shared
from matplotlib import pyplot

EEG_SIGNAL_FILE = "eeg_1min.csv"
EEG_SAMPLING_FREQUENCY = 500

BANDS_FIGURE_TITLE = "Comparison of EEG bands"
BANDS_FIGURE_SUPTITLE = "zoomed in a window of {}s"
RMS_FORMAT = "RMS of {}"

ZOOM_IN_SECONDS = 6

def splitEegBands(original_signal, eeg_bands_list, start_unfiltered=True, display_rms=False, zoom_in_seconds=ZOOM_IN_SECONDS):
    rms_list = {}
    time_range = (EEG_SAMPLING_FREQUENCY * zoom_in_seconds)
    start_index = random.randint(0, (len(original_signal) - time_range))

    pyplot.figure(BANDS_FIGURE_TITLE).suptitle(BANDS_FIGURE_SUPTITLE.format(zoom_in_seconds), size=shared.SUPTITLE_FONT_SIZE)
    pyplot.subplots_adjust(bottom=0.025, top=0.85, left=0.025, right=.975, wspace=0.05, hspace=0.25)
    axis = pyplot.subplot(3, 2, 1)

    for band in eeg_bands_list:
        _, _, eeg_band_title, eeg_band_plot_index, eeg_line_color = band
        eeg_band = shared.getEegBand(original_signal, EEG_SAMPLING_FREQUENCY, band, do_not_filter=start_unfiltered)

        axis = pyplot.subplot(3, 2, eeg_band_plot_index, sharex=axis, xticks=[], yticks=[])
        axis.set_title(eeg_band_title, size=shared.LABEL_FONT_SIZE)
        axis.set_xlim(start_index, start_index + time_range)
        pyplot.plot(eeg_band, color=eeg_line_color)

        if display_rms:
            band_rms = [shared.getRootMeanSquare(eeg_band)] * len(eeg_band)
            rms_list[eeg_band_title] = band_rms[0]
            pyplot.plot(band_rms, label=RMS_FORMAT.format(round(band_rms[0])), color=shared.COLOR_RED)
            pyplot.legend()

        start_unfiltered = False
    
    pyplot.show()
    return list(rms_list.items())

@shared.presentPoint
def main():
    noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)
    splitEegBands(noisy_eeg_signal, shared.getEegBandsList(verbose=True))

if __name__ == "__main__":
    main()