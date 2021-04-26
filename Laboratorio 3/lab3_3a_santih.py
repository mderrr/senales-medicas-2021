import shared
from matplotlib import pyplot

POINT_TITLE = "Punto 3a"
NEWBORN_SIGNAL_FILE = "apnea.csv"

NEWBORN_CSV_KEYS = ["Neonato 1", "Neonato 2"]

NEWBORN_FIGURE_TITLE = "Newborn {}"

EMG_SUPTITLE = "Extracted EMG Comparison"
ECG_SUPTITLE = "Extracted ECG Comparison"
FULL_COMPARISON_SUPTITLE = "Full Comparison"

ORIGINAL_LABEL = "Original"
EMG_LABEL = "Filtered EMG"
ECG_LABEL = "Filtered ECG"

noisy_first_newborn_signal = shared.getSignalFromFile(NEWBORN_SIGNAL_FILE, NEWBORN_CSV_KEYS[0])
noisy_second_newborn_signal = shared.getSignalFromFile(NEWBORN_SIGNAL_FILE, NEWBORN_CSV_KEYS[1])

NEWBORN_SIGNAL_SAMPLING_FREQUENCY = int(len(noisy_first_newborn_signal) / 60)

NOISY_NEWBORN_SIGNALS_LIST = [noisy_first_newborn_signal, noisy_second_newborn_signal]

EMG_HIGHPASS_FREQUENCY_CUTOFF = 60
ECG_HIGHPASS_FREQUENCY_CUTOFF = 0.5
ECG_LOWPASS_FREQUENCY_CUTOFF = 20

def showSamplingFrequencyTests():
    # Find the best low pass for EMG
    shared.testCutoffFrequencies(noisy_first_newborn_signal, NEWBORN_SIGNAL_SAMPLING_FREQUENCY, 5, 60, 16, stable_cutoff_frequency=450) # Best looking is ~60Hz

    # Find the best high pass for EMG
    shared.testCutoffFrequencies(noisy_first_newborn_signal, NEWBORN_SIGNAL_SAMPLING_FREQUENCY, 80, 450, 16, band_to_test=shared.HIGHPASS, stable_cutoff_frequency=60) # Doesn´t seem to matter that much? 

def getFilteredEmgSignal(original_signal, signal_sampling_frequency, cutoff_frequency=EMG_HIGHPASS_FREQUENCY_CUTOFF):    
    return shared.simpleFilterSignal(original_signal, signal_sampling_frequency, shared.HIGHPASS, cutoff_frequency, acount_for_dc_level=True)

def getFilteredEcgSignal(original_signal, signal_sampling_frequency, low_frequency_cutoff=ECG_HIGHPASS_FREQUENCY_CUTOFF, high_frequency_cutoff=ECG_LOWPASS_FREQUENCY_CUTOFF):    
    return shared.filterSignal(original_signal, signal_sampling_frequency, low_frequency_cutoff, high_frequency_cutoff, acount_for_dc_level=True)

def showEmgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    filtered_emg_signal = getFilteredEmgSignal(newborn_signal, newborn_signal_sampling_frequency, EMG_HIGHPASS_FREQUENCY_CUTOFF)

    figure = pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(EMG_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(2, 1, 1, yticks=[], xticks=[])

    axis.set_xlim(0, 500)
    axis.set_ylim(0.8, 3)
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.1)

    axis.set_ylabel(ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY, alpha=0.75)
    pyplot.plot(newborn_signal, color=shared.COLOR_GRAY, alpha=0.75)

    axis = pyplot.subplot(2, 1, 2, yticks=[], xticks=[], sharex=axis)
    shared.animatePlot(figure, axis, filtered_emg_signal, level_of_compression=8, x_viewing_window=500, hide_ticks=True, line_color=shared.COLOR_GREEN, y_label=EMG_LABEL, y_label_color=shared.COLOR_GREEN, y_label_font_size=shared.SUPTITLE_FONT_SIZE)

    return filtered_emg_signal

def showEcgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    filtered_ecg_signal = getFilteredEcgSignal(newborn_signal, newborn_signal_sampling_frequency, ECG_HIGHPASS_FREQUENCY_CUTOFF, ECG_LOWPASS_FREQUENCY_CUTOFF)

    figure = pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(ECG_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(2, 1, 1, yticks=[], xticks=[])

    axis.set_xlim(0, 500)
    axis.set_ylim(0.8, 3)
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.1)

    axis.set_ylabel(ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY, alpha=0.75)
    pyplot.plot(newborn_signal, color=shared.COLOR_GRAY, alpha=0.75)

    axis = pyplot.subplot(2, 1, 2, yticks=[], xticks=[], sharex=axis)
    shared.animatePlot(figure, axis, filtered_ecg_signal, level_of_compression=8, x_viewing_window=500, hide_ticks=True, line_color=shared.COLOR_RED, y_label=ECG_LABEL, y_label_color=shared.COLOR_RED, y_label_font_size=shared.SUPTITLE_FONT_SIZE)

    return filtered_ecg_signal

def showFullComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number, filtered_emg_signal, filtered_ecg_signal):
    pyplot.figure(NEWBORN_FIGURE_TITLE.format(newborn_number))
    pyplot.suptitle(FULL_COMPARISON_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    axis = pyplot.subplot(3, 1, 1, yticks=[], xticks=[])
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.08, right=0.96,  wspace=0.1, hspace=0.2)

    axis.set_ylabel(ORIGINAL_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GRAY)
    pyplot.plot(newborn_signal, label=ORIGINAL_LABEL, color=shared.COLOR_GRAY)

    axis = pyplot.subplot(3, 1, 2, yticks=[], xticks=[], sharex=axis)
    axis.set_ylabel(EMG_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_GREEN)
    pyplot.plot(filtered_emg_signal, color=shared.COLOR_GREEN)

    axis = pyplot.subplot(3, 1, 3, sharex=axis,yticks=[], xticks=[])
    axis.set_ylabel(ECG_LABEL, fontsize=shared.SUPTITLE_FONT_SIZE, color=shared.COLOR_RED)
    pyplot.plot(filtered_ecg_signal, color=shared.COLOR_RED)

    pyplot.show()

def showFiltering(newborn_signal, newborn_signal_sampling_frequency, newborn_number):
    emg_signal = showEmgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number)
    ecg_signal = showEcgComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number)
    showFullComparison(newborn_signal, newborn_signal_sampling_frequency, newborn_number, emg_signal, ecg_signal)

@shared.presentPoint
def main():
    newborn_number = 1

    showSamplingFrequencyTests()

    for newborn in NOISY_NEWBORN_SIGNALS_LIST:
        showFiltering(newborn, NEWBORN_SIGNAL_SAMPLING_FREQUENCY, newborn_number)
        newborn_number += 1

if __name__ == "__main__":
    main()