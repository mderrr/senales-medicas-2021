import numpy
import shared
from scipy import signal
from matplotlib import pyplot

FILTERED_FIGURE_TITLE = "Filtered Signal"
FREQUENCY_RESPONSE_FIGURE_TITLE = "Filter Frequency Response"
FILTERED_FIGURE_SUPTITLE = "Filtered with band-pass between {}Hz and {}Hz"

CUTOFF_FREQUENCY_LEGEND = "{} cut-off"
FREQUENCY_RESPONSE_LEGEND = "{} response"

LOW_CUTOFF_VALUE = 0.5
HIGH_CUTOFF_VALUE = 20

def showSamplingFrequencyTests(signal_array, signal_sampling_frequency):
    # Find the best low pass
    shared.testCutoffFrequencies(signal_array, signal_sampling_frequency, 19, 40, 16, show_rationale=True) # Best looking is ~20Hz

    # Find the best high pass
    shared.testCutoffFrequencies(signal_array, signal_sampling_frequency, 0.3, 1.5, 16, band_to_test=shared.HIGHPASS, stable_cutoff_frequency=20) # Best looking is ~0.5Hz

def applyPassbandFilter(signal_array, signal_sampling_frequency, low_cutoff_value, high_cutoff_value):
    filtered_ecg_signal = shared.getFilteredSignal(signal_array, signal_sampling_frequency, low_cutoff_value, high_cutoff_value, acount_for_dc_level=True)

    pyplot.figure(FILTERED_FIGURE_TITLE).suptitle(FILTERED_FIGURE_SUPTITLE.format(low_cutoff_value, high_cutoff_value), fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.subplots_adjust(bottom=0.04, top=0.925, left=0.04, right=0.96)
    pyplot.xticks([])
    pyplot.yticks([])

    pyplot.plot(signal_array, color=shared.COLOR_GRAY, alpha=0.5, label=shared.ORIGINAL_LABEL)
    pyplot.plot(filtered_ecg_signal, color=shared.COLOR_RED, label=shared.FILTERED_LABEL, linewidth=3)
    pyplot.legend()

    pyplot.show()

def showFilterFrequencyResponse(cutoff_values, sampling_rate, filter_type=shared.LOWPASS, show_plot=False):
    line_color = shared.COLOR_BLUE if filter_type == shared.LOWPASS else shared.COLOR_ORANGE
    tick_formatter = shared.getPlotTickFormatter(shared.UNIT_HERTZ)

    cutoff = cutoff_values[0] / (sampling_rate / 2)

    if len(cutoff_values) > 1:
        cutoff = [cutoff_values[0] / (sampling_rate / 2), cutoff_values[1] / (sampling_rate / 2)]

    b, a = signal.butter(4, cutoff, filter_type)
    w, h = signal.freqz(b, a)
    h = numpy.abs(h)
    w = (w * sampling_rate) / (2 * numpy.pi)
    
    pyplot.figure(FREQUENCY_RESPONSE_FIGURE_TITLE)
    axis = pyplot.subplot(1, 1, 1)
    axis.xaxis.set_major_formatter(tick_formatter)
    pyplot.subplots_adjust(bottom=0.08, top=0.96, left=0.08, right=0.96)

    pyplot.axvline(x=cutoff_values[0], color=line_color, alpha=0.8, label=CUTOFF_FREQUENCY_LEGEND.format(filter_type), linestyle=shared.LINESTYLE_DASHED)

    if len(cutoff_values) > 1:
        pyplot.axvline(x=cutoff_values[1], color=line_color, alpha=0.8, linestyle=shared.LINESTYLE_DASHED)
        pyplot.fill_between(w, h, color='blue', alpha=0.3)

    pyplot.plot(w, h, label=FREQUENCY_RESPONSE_LEGEND.format(filter_type), linewidth=3)

    pyplot.xlim(0, 50)
    pyplot.legend()

    if show_plot: pyplot.show()

def showFrequencyReponsePlot(low_cutoff_value, high_cutoff_value, signal_sampling_frequency):
    showFilterFrequencyResponse([high_cutoff_value], signal_sampling_frequency)
    showFilterFrequencyResponse([low_cutoff_value], signal_sampling_frequency, filter_type=shared.HIGHPASS, show_plot=True)
    
    showFilterFrequencyResponse([low_cutoff_value, high_cutoff_value], signal_sampling_frequency, filter_type=shared.BANDPASS, show_plot=True)

@shared.presentPoint
def main():
    noisy_ecg_signal = shared.getSignalFromFile(shared.ECG_FILE_NAME)

    showSamplingFrequencyTests(noisy_ecg_signal, shared.ECG_SAMPLING_FREQUENCY)
    applyPassbandFilter(noisy_ecg_signal, shared.ECG_SAMPLING_FREQUENCY, LOW_CUTOFF_VALUE, HIGH_CUTOFF_VALUE)
    showFrequencyReponsePlot(LOW_CUTOFF_VALUE, HIGH_CUTOFF_VALUE, shared.ECG_SAMPLING_FREQUENCY)

if __name__ == "__main__":
    main()