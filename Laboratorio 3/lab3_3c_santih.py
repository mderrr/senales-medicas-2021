import numpy
import shared
from matplotlib import pyplot

NEWBORN_NAME_FORMAT = "neonato {}"
NEWBORN_FIGURE_TITLE = "Newborn {}"

PEAKS_SUPTITLE = "Extracted Peaks From Newborn {}'s ECG"
EMG_PROCESSING_SUPTITLE = "Tranformations applied to newborn {}'s EMG Signal"

BREATHING_RATE_MESSAGE = "La frequencia respiratoria del neonato {} es de {} Respiraciones/min."
BREATHING_RATE_POPUP_MESSAGE = "La frequencia respiratoria del {} esta {} con {} de {} {}"

DEFAULT_CONVOLVE_MODE = "same"

# Signal smoothing with RMS envelope
def getRmsEnvelopedSignal(signal_array, window_size=None, convolve_mode=None):
    window_size = window_size if window_size is not None else 400 # A size of 400 for the window seems to give best looking and most accurate result
    convolve_mode = convolve_mode if convolve_mode is not None else DEFAULT_CONVOLVE_MODE

    squared_signal_array = signal_array ** 2
    window_array = numpy.ones(window_size) / float(window_size) # To make every item 1 / window_size

    return numpy.sqrt(numpy.convolve(squared_signal_array, window_array, convolve_mode))

def rectifyAndEnvelopeSignal(signal_array, signal_sampling_frequency, patient_number=0, envelope_window_size=None, envelope_convolve_mode=None):
    dc_removed_signal = signal_array - numpy.mean(signal_array)
    rectified_signal = numpy.absolute(dc_removed_signal) # Rectify the signal
    rms_enveloped_signal = getRmsEnvelopedSignal(rectified_signal, window_size=envelope_window_size, convolve_mode=envelope_convolve_mode)
    line_at_zero = [0] * len(signal_array)

    pyplot.figure(NEWBORN_FIGURE_TITLE.format(patient_number))
    pyplot.suptitle(EMG_PROCESSING_SUPTITLE.format(patient_number), fontsize=shared.SUPTITLE_FONT_SIZE)
    axis = pyplot.subplot(2, 1, 1, yticks=[0], xticks=[])
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.05, right=0.95,  wspace=0.1, hspace=0.1)

    pyplot.plot(signal_array, label=shared.ORIGINAL_LABEL, color=shared.COLOR_GRAY, alpha=0.5)
    pyplot.plot(line_at_zero, color=shared.COLOR_BLACK, alpha=0.5)
    pyplot.legend()

    axis = pyplot.subplot(2, 1, 2, yticks=[0], xticks=[], sharex=axis)
    pyplot.plot(rectified_signal, label=shared.RECTIFIED_LABEL, color=shared.COLOR_LIGHTGREEN)
    pyplot.plot(rms_enveloped_signal, label=shared.ENVELOPED_LABEL, color=shared.COLOR_GREEN)
    pyplot.plot(line_at_zero, color=shared.COLOR_BLACK, alpha=0.5)
    pyplot.legend()

    pyplot.show()

    return rms_enveloped_signal

def calculateBreathingRate(signal_array, signal_sampling_frequency, newborn_number, prominence_factor=None):
    prominence_factor = prominence_factor if prominence_factor is not None else 0.025 # About 2.5% prominence looks right

    filtered_emg_signal = shared.simpleFilterSignal(signal_array, signal_sampling_frequency, shared.HIGHPASS, 60, acount_for_dc_level=True)
    rms_enveloped_emg_signal = rectifyAndEnvelopeSignal(filtered_emg_signal, signal_sampling_frequency, newborn_number)

    signal_peaks_array = shared.extractPeaksFromSignal(rms_enveloped_emg_signal, signal_sampling_frequency, prominence_factor=prominence_factor)
    shared.showExtractedPeaks(filtered_emg_signal, signal_peaks_array, newborn_number, NEWBORN_FIGURE_TITLE, PEAKS_SUPTITLE, line_color=shared.COLOR_GREEN)

    newborn_breathing_rate = shared.getPeakRate(signal_peaks_array, signal_sampling_frequency)
    shared.displayPopUp(BREATHING_RATE_MESSAGE.format(newborn_number, newborn_breathing_rate))

    return {shared.BREATHING_RATE_KEY: newborn_breathing_rate}

@shared.presentPoint
def main():
    noisy_first_newborn_signal, noisy_second_newborn_signal, newborn_signals_list, newborn_signal_sampling_rate = shared.getApneaData()

    for newborn_signal in newborn_signals_list:
        newborn_number = newborn_signals_list.index(newborn_signal) + 1

        newborn_breathing_rate = calculateBreathingRate(newborn_signal, newborn_signal_sampling_rate, newborn_number)
        shared.checkVitals(newborn_breathing_rate, shared.NORMAL_NEWBORN_VITAL_SIGNS, BREATHING_RATE_POPUP_MESSAGE, patient_name=NEWBORN_NAME_FORMAT.format(newborn_number))

if __name__ == "__main__":
    main()