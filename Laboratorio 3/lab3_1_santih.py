import shared
from scipy import signal
from matplotlib import pyplot
import numpy

ECG_SIGNAL_FILE = "ecg_noisy2.csv"
ECG_SAMPLING_FREQUENCY = 1000

ORIGINAL_LABEL = "Original"
FILTERED_LABEL = "Filtered"

FILTERED_FIGURE_TITLE = "Filtered Signal"
FREQUENCY_RESPONSE_FIGURE_TITLE = "Filter Frequency Response"
FILTERED_FIGURE_SUPTITLE = "Filtered with band-pass between {}Hz and {}Hz"

CUTOFF_FREQUENCY_LEGEND = "{} cut-off"

FREQUENCY_RESPONSE_LEGEND = "{} response"

LOW_CUTOFF_VALUE = 0.5
HIGH_CUTOFF_VALUE = 20

noisy_ecg_signal = shared.getSignalFromFile(ECG_SIGNAL_FILE)

def showSamplingFrequencyTests():
    # Find the best low pass
    shared.testCutoffFrequencies(noisy_ecg_signal, ECG_SAMPLING_FREQUENCY, 0.25, 1.5, 16) # Best looking is ~0.5Hz

    # Find the best high pass
    shared.testCutoffFrequencies(noisy_ecg_signal, ECG_SAMPLING_FREQUENCY, 19, 40, 16, band_to_test=shared.HIGHPASS, stable_cutoff_frequency=0.5) # Best looking is ~20Hz

def applyPassbandFilter():
    filtered_ecg_signal = shared.filterSignal(noisy_ecg_signal, ECG_SAMPLING_FREQUENCY, LOW_CUTOFF_VALUE, HIGH_CUTOFF_VALUE, acount_for_dc_level=True)

    pyplot.figure(FILTERED_FIGURE_TITLE).suptitle(FILTERED_FIGURE_SUPTITLE.format(LOW_CUTOFF_VALUE, HIGH_CUTOFF_VALUE), fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.subplots_adjust(bottom=0.04, top=0.925, left=0.04, right=0.96)
    pyplot.xticks([])
    pyplot.yticks([])

    pyplot.plot(noisy_ecg_signal, color=shared.COLOR_GRAY, alpha=0.5, label=ORIGINAL_LABEL)
    pyplot.plot(filtered_ecg_signal, color=shared.COLOR_RED, label=FILTERED_LABEL, linewidth=3)
    pyplot.legend()

    pyplot.show()

def showFilterFrequencyResponse(cutoff_value, sampling_rate, filter_type=shared.LOWPASS, show_plot=False):
    cutoff = cutoff_value / (sampling_rate / 2)
    b, a = signal.butter(4, cutoff, filter_type)
    w, h = signal.freqz(b, a)
    h = numpy.abs(h)
    w = (w * sampling_rate) / (2 * numpy.pi)
    tick_formatter = shared.getPlotTickFormatter(shared.HERTZ)
    line_color = shared.COLOR_BLUE if filter_type == shared.LOWPASS else shared.COLOR_ORANGE

    pyplot.figure(FREQUENCY_RESPONSE_FIGURE_TITLE)
    axis = pyplot.subplot(1, 1, 1)
    axis.xaxis.set_major_formatter(tick_formatter)
    pyplot.subplots_adjust(bottom=0.08, top=0.96, left=0.08, right=0.96)
    pyplot.axvline(x=cutoff_value, color=line_color, alpha=0.8, label=CUTOFF_FREQUENCY_LEGEND.format(filter_type), linestyle=shared.LINESTYLE_DASHED)

    pyplot.plot(w, h, label=FREQUENCY_RESPONSE_LEGEND.format(filter_type), linewidth=3)

    pyplot.legend()
    pyplot.grid()
    pyplot.xlim(0, 50)
    if show_plot: pyplot.show()

@shared.presentPoint
def main():
    showSamplingFrequencyTests()
    applyPassbandFilter()
    showFilterFrequencyResponse(HIGH_CUTOFF_VALUE, ECG_SAMPLING_FREQUENCY)
    showFilterFrequencyResponse(LOW_CUTOFF_VALUE, ECG_SAMPLING_FREQUENCY, filter_type=shared.HIGHPASS, show_plot=True)

if __name__ == "__main__":
    main()