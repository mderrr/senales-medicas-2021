import shared
from matplotlib import pyplot

NEWBORN_FIGURE_TITLE = "Newborn {}"
NEWBORN_NAME_FORMAT = "neonato {}"
PEAKS_SUPTITLE = "Extracted Peaks From Newborn {}'s ECG"

HEART_RATE_MESSAGE = "La frequencia cardiaca del neonato {} es de {} Lpm."
HEART_RATE_POPUP_MESSAGE = "La frequencia cardiaca del {} esta {} con {} de {} {}"

def calculateHeartRate(signal_array, signal_sampling_frequency, newborn_number, prominence_factor=None):
    filtered_ecg_signal = shared.getFilteredSignal(signal_array, signal_sampling_frequency, 0.5, 20, acount_for_dc_level=True)
    signal_peaks_array = shared.extractPeaksFromSignal(filtered_ecg_signal, signal_sampling_frequency, prominence_factor=prominence_factor)
    newborn_heart_rate = shared.getPeakRate(signal_peaks_array, signal_sampling_frequency)

    shared.showExtractedPeaks(filtered_ecg_signal, signal_peaks_array, newborn_number, NEWBORN_FIGURE_TITLE, PEAKS_SUPTITLE)
    shared.displayPopUp(HEART_RATE_MESSAGE.format(newborn_number, newborn_heart_rate))

    return {shared.HEART_RATE_KEY: newborn_heart_rate}

@shared.presentPoint
def main():
    noisy_first_newborn_signal, noisy_second_newborn_signal, newborn_signals_list, newborn_signal_sampling_rate = shared.getApneaData()

    for newborn_signal in newborn_signals_list:
        newborn_number = newborn_signals_list.index(newborn_signal) + 1

        newborn_heart_rate = calculateHeartRate(newborn_signal, newborn_signal_sampling_rate, newborn_number)
        shared.checkVitals(newborn_heart_rate, shared.NORMAL_NEWBORN_VITAL_SIGNS, HEART_RATE_POPUP_MESSAGE, patient_name=NEWBORN_NAME_FORMAT.format(newborn_number))

if __name__ == "__main__":
    main()