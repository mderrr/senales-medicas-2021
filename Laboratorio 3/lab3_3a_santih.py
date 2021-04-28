import shared
from matplotlib import pyplot

NEWBORN_FIGURE_TITLE = "Newborn {}"

EMG_SUPTITLE = "Extracted EMG Comparison"
ECG_SUPTITLE = "Extracted ECG Comparison"
FULL_COMPARISON_SUPTITLE = "Full Comparison"

EMG_HIGHPASS_FREQUENCY_CUTOFF = 60
ECG_HIGHPASS_FREQUENCY_CUTOFF = 0.5
ECG_LOWPASS_FREQUENCY_CUTOFF = 20

ANIMATION_LEVEL_OF_COMPRESSION = 8

def showSamplingFrequencyTests(signal_array, signal_sampling_frequency):
    # Find the best low pass for EMG
    shared.testCutoffFrequencies(signal_array, signal_sampling_frequency, 80, 450, 16, stable_cutoff_frequency=60, show_rationale=True) # Doesn´t seem to matter that much? 

    # Find the best high pass for EMG
    shared.testCutoffFrequencies(signal_array, signal_sampling_frequency, 5, 60, 16, band_to_test=shared.HIGHPASS, stable_cutoff_frequency=450) # Best looking is ~60Hz

def showEmgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    filtered_emg_signal = shared.getSimpleFilteredSignal(newborn_signal, newborn_signal_sampling_frequency, shared.HIGHPASS, EMG_HIGHPASS_FREQUENCY_CUTOFF, acount_for_dc_level=True)

    figure = pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(EMG_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(2, 1, 1, yticks=[], xticks=[])

    axis.set_xlim(0, 500)
    axis.set_ylim(0.8, 3)
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.1)

    axis.set_ylabel(shared.ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY, alpha=0.75)
    pyplot.plot(newborn_signal, color=shared.COLOR_GRAY, alpha=0.75)

    axis = pyplot.subplot(2, 1, 2, yticks=[], xticks=[], sharex=axis)
    shared.animatePlot(figure, axis, filtered_emg_signal, level_of_compression=ANIMATION_LEVEL_OF_COMPRESSION, x_viewing_window=500, hide_ticks=True, line_color=shared.COLOR_GREEN, y_label=shared.EMG_LABEL, y_label_color=shared.COLOR_GREEN, y_label_font_size=shared.SUPTITLE_FONT_SIZE)

    return filtered_emg_signal

def showEcgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    filtered_ecg_signal = shared.getFilteredSignal(newborn_signal, newborn_signal_sampling_frequency, ECG_HIGHPASS_FREQUENCY_CUTOFF, ECG_LOWPASS_FREQUENCY_CUTOFF, acount_for_dc_level=True)

    figure = pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(ECG_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(2, 1, 1, yticks=[], xticks=[])

    axis.set_xlim(0, 500)
    axis.set_ylim(0.8, 3)
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.1)

    axis.set_ylabel(shared.ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY, alpha=0.75)
    pyplot.plot(newborn_signal, color=shared.COLOR_GRAY, alpha=0.75)

    axis = pyplot.subplot(2, 1, 2, yticks=[], xticks=[], sharex=axis)
    shared.animatePlot(figure, axis, filtered_ecg_signal, level_of_compression=ANIMATION_LEVEL_OF_COMPRESSION, x_viewing_window=500, hide_ticks=True, line_color=shared.COLOR_RED, y_label=shared.ECG_LABEL, y_label_color=shared.COLOR_RED, y_label_font_size=shared.SUPTITLE_FONT_SIZE)

    return filtered_ecg_signal

def showFullComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number, filtered_emg_signal, filtered_ecg_signal):
    pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(FULL_COMPARISON_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(3, 1, 1, yticks=[], xticks=[])
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.2)

    axis.set_ylabel(shared.ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY)
    pyplot.plot(newborn_signal, label=shared.ORIGINAL_LABEL, color=shared.COLOR_GRAY)

    axis = pyplot.subplot(3, 1, 2, yticks=[], xticks=[], sharex=axis)
    axis.set_ylabel(shared.EMG_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GREEN)
    pyplot.plot(filtered_emg_signal, color=shared.COLOR_GREEN)

    axis = pyplot.subplot(3, 1, 3, sharex=axis,yticks=[], xticks=[])
    axis.set_ylabel(shared.ECG_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_RED)
    pyplot.plot(filtered_ecg_signal, color=shared.COLOR_RED)

    pyplot.show()

def showFiltering(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    emg_signal = showEmgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number)
    ecg_signal = showEcgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number)
    
    showFullComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number, emg_signal, ecg_signal)

@shared.presentPoint
def main():
    noisy_first_newborn_signal, noisy_second_newborn_signal, newborn_signals_list, newborn_signal_sampling_rate = shared.getApneaData()
    
    showSamplingFrequencyTests(noisy_first_newborn_signal, newborn_signal_sampling_rate)

    for newborn_signal in newborn_signals_list:
        newborn_number = newborn_signals_list.index(newborn_signal) + 1
        showFiltering(newborn_signal, newborn_signal_sampling_rate, newborn_number)

if __name__ == "__main__":
    main()