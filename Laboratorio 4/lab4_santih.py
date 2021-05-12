import pandas, numpy, os
from scipy import signal
from matplotlib import pyplot

CURRENT_FILE_DIRECTORY = os.path.dirname(__file__)
ECG_FILE_FORMAT = "./ecg{}.csv"
ECG_FIGURE_TITLE = "ECG {}"
ECG_TITLE = "Peaks extrated from ECG {}'s signal"
HEART_RATE_LABEL = "Heart Rate: {} Bpm"
HEART_RATE_MESSAGE = "El ECG {} tiene una frecuencia cardiaca de {}Lpm"
RO ="ro"

def setCurrentWorkingDirectory():
    if (CURRENT_FILE_DIRECTORY != os.getcwd()):
        os.chdir(CURRENT_FILE_DIRECTORY)

def getSignalFromFile(file_name, dict_key=""):
    file_dictionary = pandas.read_csv(file_name)
    if not dict_key: dict_key = list(file_dictionary.keys())[0]
    
    return file_dictionary[dict_key], dict_key

def getSignalSampligRate(data_frame_key):
    sampling_rate = int(data_frame_key[5:-3])

    return sampling_rate

def getFilteredSignal(noisy_signal, signal_samping_rate, low_cutoff_value=1, high_cutoff_value=25, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0
    low_cutoff = low_cutoff_value / (signal_samping_rate / 2)
    high_cutoff = high_cutoff_value / (signal_samping_rate / 2)
    cutoff_frequencies = [low_cutoff, high_cutoff]
    b, a = signal.butter(4, cutoff_frequencies, "bandpass")

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal

def removeOutliers(signal):
    normalized_signal = numpy.copy(signal)
    normalized_signal = numpy.where(normalized_signal > (numpy.mean(normalized_signal) + 10 * numpy.std(normalized_signal)), numpy.mean(normalized_signal), normalized_signal)
    normalized_signal = numpy.where(normalized_signal < (numpy.mean(normalized_signal) - 10 * numpy.std(normalized_signal)), numpy.mean(normalized_signal), normalized_signal)

    return normalized_signal

def getPeakRate(signal_peaks_array, signal_sampling_frequency, signal_duration_in_seconds=60):
        instant_peak_rates_array = []
        sampling_period = 1 / signal_sampling_frequency
        
        for peak in signal_peaks_array:
            current_peak_index = signal_peaks_array.index(peak)
            previous_peak = signal_peaks_array[current_peak_index - 1]

            if (current_peak_index == 0): # Ignore first peak
                continue

            peak_difference = peak - previous_peak

            peak_duration = peak_difference * sampling_period
            instant_peak_rate = (1 / peak_duration) * signal_duration_in_seconds

            instant_peak_rates_array.append(instant_peak_rate)

        return round(numpy.mean(instant_peak_rates_array))

def showSignals():
    for ecg_file in range(1, 8):
        ecg_signal, dict_key = getSignalFromFile(ECG_FILE_FORMAT.format(ecg_file))
        signal_sampling_rate = getSignalSampligRate(dict_key)
        ecg_signal = removeOutliers(ecg_signal)
        ecg_signal = getFilteredSignal(ecg_signal, signal_sampling_rate)

        ecg_signal -= numpy.min(ecg_signal)
        ecg_signal /= numpy.max(ecg_signal)

        peaks, _ = signal.find_peaks(ecg_signal, prominence=0.25)
        peaks = list(peaks)

        for i in range(len(peaks) - 1):
            if i == 0: continue
            peak = peaks[i]
            peak_prev = peaks[i-1]

            if (peak - peak_prev < 275): 
                peaks[i] = peak_prev

        frequency = getPeakRate(peaks, signal_sampling_rate)
        print(HEART_RATE_MESSAGE.format(ecg_file, frequency))

        pyplot.figure(ECG_FIGURE_TITLE.format(ecg_file))
        pyplot.title(ECG_TITLE.format(ecg_file))
        pyplot.plot(ecg_signal)
        pyplot.plot(peaks, ecg_signal[peaks], RO, label=HEART_RATE_LABEL.format(frequency))
        pyplot.legend()

    pyplot.show()

setCurrentWorkingDirectory()
showSignals()