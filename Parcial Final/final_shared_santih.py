import os
import sys
import numpy
import pandas
import platform
from scipy import signal
from fnmatch import fnmatch
from matplotlib.ticker import EngFormatter as plotTickFormatter

WINDOWS_PLATFORM_NAME    = "Windows"
WINDOWS_CLEAR            = "cls"
UNIX_CLEAR               = "clear"

COLOR_GRAY               = "gray"
COLOR_BLACK              = "black"
COLOR_GREEN              = "green"
COLOR_LIGHTGREEN         = "limegreen"

ORIGINAL_LABEL           = "Original"
RECTIFIED_LABEL          = "Rectified"
ENVELOPED_LABEL          = "RMS Enveloped"

BLUE_OBJECT = "bo"
GREEN_OBJECT = "go"
RED_OBJECT = "ro"

WINDOWS_EXECUTE_TEMPLATE = "py .\{}"
UNIX_EXECUTE_TEMPLATE    = "python3 './{}'"

POINT_TITLE_TEMPLATE     = "////////////////  Punto {}  ////////////////"

SUPTITLE_FONT_SIZE       = 16
LABEL_FONT_SIZE          = 14

CURRENT_FILE_DIRECTORY   = os.path.dirname(__file__)

def getFilteredSignal(noisy_signal, signal_samping_rate, low_cutoff_value=0.5, high_cutoff_value=20, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0
    low_cutoff = low_cutoff_value / (signal_samping_rate / 2)
    high_cutoff = high_cutoff_value / (signal_samping_rate / 2)
    cutoff_frequencies = [low_cutoff, high_cutoff]
    b, a = signal.butter(4, cutoff_frequencies, "bandpass")

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal

def setCurrentWorkingDirectory():
    if (CURRENT_FILE_DIRECTORY != os.getcwd()):
        os.chdir(CURRENT_FILE_DIRECTORY)

def clear(title=""):
    os.system(WINDOWS_CLEAR if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_CLEAR)
    if title: print(POINT_TITLE_TEMPLATE.format(title))

def getPythonName():
    python_name = WINDOWS_EXECUTE_TEMPLATE if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_EXECUTE_TEMPLATE
   
    return python_name

def getPointName():
    return os.path.basename(sys.argv[0]).split("_")[1]

def getPlotTickFormatter(units, separator=""):
    return plotTickFormatter(unit=units, sep=separator)

def getSignalFromFile(file_name, dict_key=None):
    file_dictionary = pandas.read_csv(file_name)
    dict_key = dict_key if dict_key is not None else list(file_dictionary.keys())[0]
    
    return file_dictionary[dict_key]

def presentPoint(main_function):
    point_name = getPointName()
    clear(point_name)

    return main_function

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

def getPeakPeriods(signal_peaks_array, signal_sampling_frequency, signal_duration_in_seconds=60):
        instant_peak_durations_array = []
        sampling_period = 1 / signal_sampling_frequency
        
        for peak in signal_peaks_array:
            current_peak_index = signal_peaks_array.index(peak)
            previous_peak = signal_peaks_array[current_peak_index - 1]

            if (current_peak_index == 0): # Ignore first peak
                continue

            peak_difference = peak - previous_peak
            peak_duration = peak_difference * sampling_period

            instant_peak_durations_array.append(peak_duration)

        return instant_peak_durations_array

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

def extractPeaksFromSignal(signal_array, prominence_factor=None):
    prominence_factor = prominence_factor if prominence_factor is not None else 0.25 # About 25% prominence seems to do the trick for both ECGs

    return list(signal.find_peaks(signal_array, prominence=prominence_factor)[0]) # Good thing someone already did the hard work

def findFilesOnDirectory(file_pattern, path):
    found_items_list = []

    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, file_pattern):
                found_items_list.append(os.path.basename(os.path.join(root, name)))

    return sorted(found_items_list)

setCurrentWorkingDirectory()