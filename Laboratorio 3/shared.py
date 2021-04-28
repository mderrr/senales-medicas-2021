import os
import sys
import numpy
import pandas
import platform
from scipy import signal
from fnmatch import fnmatch
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from tkinter import Tk, messagebox, Toplevel, Label, Button
from matplotlib.ticker import EngFormatter as plotTickFormatter

ECG_FILE_NAME = "./ecg_noisy2.csv"
EEG_FILE_NAME = "./eeg_1min.csv"
APNEA_FILE_NAME = "./apnea.csv"

WINDOWS_PLATFORM_NAME = "Windows"
WINDOWS_CLEAR = "cls"
UNIX_CLEAR = "clear"

BANDPASS = "bandpass"
LOWPASS = "lowpass"
HIGHPASS = "highpass"

COLOR_BLACK = "black"
COLOR_GRAY = "gray"
COLOR_RED = "red"
COLOR_GREEN = "green"
COLOR_LIGHTGREEN = "limegreen"
COLOR_ORANGE = "orange"
COLOR_BLUE = "blue"
COLOR_YELLOW = "yellow"

UNIT_HERTZ = "Hz"
UNIT_BEATS_PER_MINUTE = "Latidos/min"
UNIT_BREATHS_PER_MINUTE = "Respiraciones/min"

LINESTYLE_DASHED = "dashed"

HEART_RATE_KEY = "Heart Rate"
BREATHING_RATE_KEY = "Breathing Rate"

INFO_POPUP_TYPE = "info"
WARNING_POPUP_TYPE = "warning"
ALERT_POPUP_TYPE = "error"

INFO_POPUP_TITLE = "información"
WARNING_POPUP_TITLE = "advertencia"
ALERT_POPUP_TITLE = "ALERTA"

TEST_SAMPLES_TITLE = "(TEST) samples for {} band (TEST)"
TEST_FRECUENCY_TITLE = "~{}Hz"
DEFAULT_EXTRACTED_PEAKS_TITLE = "Patient {}"

POINT_TITLE_TEMPLATE = "////////////////  Punto {}  ////////////////"

DEFAULT_EXTRACTED_PEAKS_SUPTITLE = "Extracted Peaks From Patient {}'s Signal"

DEFAULT_POPUP_MESSAGE="Info"

DEFAULT_PATIENT_NAME = "paciente"

LOW_VITAL_SIGN_STATUS = "BAJA"
HIGH_VITAL_SIGN_STATUS = "ALTA"
HIGH_VITAL_SIGN_CRITICAL = "MUY "
GREATER_THAN = "más"
LESSER_THAN = "menos"

ORIGINAL_LABEL = "Original"
SIGNAL_LABEL = "Signal"
PEAK_LABEL = "Peak"
FILTERED_LABEL = "Filtered"
EMG_LABEL = "Filtered EMG"
ECG_LABEL = "Filtered ECG"
RECTIFIED_LABEL = "Rectified"
ENVELOPED_LABEL = "RMS Enveloped"

INVALID_FILTER_TYPE_ERROR = "The argument: '{}' was not recognized, valid arguments are: 'lowpass' or 'highpass'."

CUTOFF_FREQUENCY_TEST_RATIONALE = "Estas gráficas solo son una herramienta para la selección de los valores de los filtros, las dejé para evidencia del proceso"

RENSPONSE_WINDOW_TITLE = "Respuesta Al Punto {}"

TK_CLOSE_WINDOW_ACTION = "WM_DELETE_WINDOW"

BOTH = "both"
CENTER = "center"
RIGHT = "right"
ARIAL= "Arial"

WINDOWS_EXECUTE_TEMPLATE = "py .\{}"
UNIX_EXECUTE_TEMPLATE = "python3 './{}'"

BUTTON_TEXT_CONTINUE = "Continuar"

APNEA_CSV_KEYS = [
    "Neonato 1",
    "Neonato 2"
]

EEG_BAND_NAMES = [
    "Original Signal",
    "Gamma: 30Hz to 100Hz+",
    "Beta: 12Hz to 30Hz", 
    "Alpha: 8Hz to 12Hz",
    "Theta: 4Hz to 7Hz", 
    "Delta: 0Hz to 4Hz"
]

COLORS_BLUE_GRADIENT = [
    "midnightblue",
    "navy",
    "darkblue",
    "mediumblue",
    "blue",
    "royalblue"
]

FONT_ARIAL = {
    10: (ARIAL, 10),
    15: (ARIAL, 15)
}

NORMAL_NEWBORN_VITAL_SIGNS = {
    HEART_RATE_KEY: (120, 160, UNIT_BEATS_PER_MINUTE),
    BREATHING_RATE_KEY: (40, 60, UNIT_BREATHS_PER_MINUTE)
}

POPUP_TITLES = {
    INFO_POPUP_TYPE: INFO_POPUP_TITLE,
    WARNING_POPUP_TYPE: WARNING_POPUP_TITLE,
    ALERT_POPUP_TYPE: ALERT_POPUP_TITLE
}

ECG_SAMPLING_FREQUENCY = 1000
EEG_SAMPLING_FREQUENCY = 500

LOW_CUTOFF_VALUE = 0.5
HIGH_CUTOFF_VALUE = 25

SUPTITLE_FONT_SIZE = 16
LABEL_FONT_SIZE = 14

CURRENT_FILE_DIRECTORY = os.path.dirname(__file__)

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

def findFilesOnDirectory(file_pattern, path):
    found_items_list = []

    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch(name, file_pattern):
                found_items_list.append(os.path.basename(os.path.join(root, name)))

    return sorted(found_items_list)

def presentPoint(main_function):
    point_name = getPointName()
    clear(point_name)

    return main_function

def getSignalFromFile(file_name, dict_key=""):
    file_dictionary = pandas.read_csv(file_name)
    if not dict_key: dict_key = list(file_dictionary.keys())[0]
    
    return file_dictionary[dict_key]

def getRootMeanSquare(signal):
    squared_signal = signal ** 2
    rms_value = numpy.sqrt(numpy.sum(squared_signal) / len(squared_signal))

    return rms_value

def getPlotTickFormatter(units, separator=""):
    return plotTickFormatter(unit=units, sep=separator)

def getSignalFft(signal_array, signal_sampling_rate):
    signal_array_size = len(signal_array)
    signal_array -= numpy.mean(signal_array)
    transformed_signal = numpy.abs(numpy.fft.fft(signal_array))
    frequency_array = (signal_sampling_rate) * (numpy.arange(1, signal_array_size + 1) / signal_array_size)

    return frequency_array, transformed_signal

def getApneaData():
    noisy_first_newborn_signal = getSignalFromFile(APNEA_FILE_NAME, APNEA_CSV_KEYS[0])
    noisy_second_newborn_signal = getSignalFromFile(APNEA_FILE_NAME, APNEA_CSV_KEYS[1])
    newborn_signals_list = [list(noisy_first_newborn_signal), list(noisy_second_newborn_signal)]
    newborn_signal_sampling_rate = int(len(noisy_first_newborn_signal) / 60)

    return noisy_first_newborn_signal, noisy_second_newborn_signal, newborn_signals_list, newborn_signal_sampling_rate

def getSimpleFilteredSignal(noisy_signal, signal_samping_rate, filter_type, cutoff_value, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0

    cutoff = cutoff_value / (signal_samping_rate / 2)
    b, a = signal.butter(4, cutoff, filter_type)

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal

def getFilteredSignal(noisy_signal, signal_samping_rate, low_cutoff_value=LOW_CUTOFF_VALUE, high_cutoff_value=HIGH_CUTOFF_VALUE, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0
    low_cutoff = low_cutoff_value / (signal_samping_rate / 2)
    high_cutoff = high_cutoff_value / (signal_samping_rate / 2)
    cutoff_frequencies = [low_cutoff, high_cutoff]
    b, a = signal.butter(4, cutoff_frequencies, BANDPASS)

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal

def getEegBandsList(verbose=False):
    eeg_band_names = EEG_BAND_NAMES

    if not verbose:
        for i in range(len(eeg_band_names)):
            eeg_band_names[i] = eeg_band_names[i].split(":")[0]

    return [
        (0, 0, eeg_band_names[0], 1, COLORS_BLUE_GRADIENT[0]),
        (30, 0 , eeg_band_names[1], 3, COLORS_BLUE_GRADIENT[1]),
        (12, 30 , eeg_band_names[2], 5, COLORS_BLUE_GRADIENT[2]),
        (8, 12 , eeg_band_names[3], 2, COLORS_BLUE_GRADIENT[3]),
        (4, 7 , eeg_band_names[4], 4, COLORS_BLUE_GRADIENT[4]),
        (0, 4 , eeg_band_names[5], 6,COLORS_BLUE_GRADIENT[5])
    ]

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

def getEegBand(noisy_signal, signal_sampling_rate, eeg_band_data, return_fft=False, do_not_filter=False):
    filter_type = BANDPASS
    lower_bound, higher_bound, _, _, _ = eeg_band_data
    low_cutoff = lower_bound / (signal_sampling_rate / 2)
    high_cutoff = higher_bound / (signal_sampling_rate / 2)

    if (lower_bound < 1):
        cutoff_frequencies = high_cutoff
        filter_type = LOWPASS

    elif (higher_bound == 0):
        cutoff_frequencies = low_cutoff
        filter_type = HIGHPASS

    else:
        cutoff_frequencies = [low_cutoff, high_cutoff]

    if do_not_filter:
        filtered_signal = noisy_signal
    else:
        b, a = signal.butter(5, cutoff_frequencies, filter_type)
        filtered_signal = signal.filtfilt(b, a, noisy_signal) 

    if (return_fft):
        return getSignalFft(filtered_signal, signal_sampling_rate)

    return filtered_signal

def createTkRoot():
    root = Tk()
    root.withdraw()

    return root

def displayResponse(response):
    def onResponseWindowClosing(root):
        root.destroy()

    point_name = getPointName()

    root = createTkRoot()
    response_window = Toplevel()
    response_window.minsize(300, 0)
    response_window.maxsize(600, 0)
    response_window.title(RENSPONSE_WINDOW_TITLE.format(point_name))
    response_window.protocol(TK_CLOSE_WINDOW_ACTION, lambda: onResponseWindowClosing(root))
    
    Label(response_window, text=response, wraplength=500, font=FONT_ARIAL[15], justify=CENTER).pack(ipadx=20, ipady=0, fill=BOTH, expand=True)
    Button(response_window, text=BUTTON_TEXT_CONTINUE, font=FONT_ARIAL[10], command=root.destroy).pack(pady=10, padx=10, ipadx=30, side=RIGHT)

    root.mainloop()

def displayPopUp(popup_message, popup_title=None, message_type=None):
    message_type = message_type if message_type is not None else INFO_POPUP_TYPE
    popup_title = popup_title if popup_title is not None else POPUP_TITLES[message_type]

    createTkRoot()
    if message_type == INFO_POPUP_TYPE: messagebox.showinfo(popup_title, popup_message)
    elif message_type == WARNING_POPUP_TYPE: messagebox.showwarning(popup_title, popup_message)
    elif message_type == ALERT_POPUP_TYPE: messagebox.showerror(popup_title, popup_message)

def extractPeaksFromSignal(signal_array, signal_sampling_frequency, prominence_factor=None):
    prominence_factor = prominence_factor if prominence_factor is not None else 0.25 # About 25% prominence seems to do the trick for both ECGs

    return list(signal.find_peaks(signal_array, prominence=prominence_factor)[0]) # Good thing someone already did the hard work

def showExtractedPeaks(signal_array, signal_peaks_array, patient_number, plot_figure_title=None, plot_figure_suptitle=None, line_color=COLOR_RED):
    plot_figure_title = plot_figure_title if plot_figure_title is not None else DEFAULT_EXTRACTED_PEAKS_TITLE
    plot_figure_suptitle = plot_figure_suptitle if plot_figure_suptitle is not None else DEFAULT_EXTRACTED_PEAKS_SUPTITLE

    pyplot.figure(plot_figure_title.format(patient_number))
    pyplot.suptitle(plot_figure_suptitle.format(patient_number), fontsize=SUPTITLE_FONT_SIZE)
    pyplot.subplots_adjust(bottom=0.05, top=0.925, left=0.05, right=0.95,  wspace=0.1, hspace=0.1)
    pyplot.xlim(0, 1000)
    pyplot.xticks([])
    pyplot.yticks([])

    pyplot.plot(signal_array, label=SIGNAL_LABEL, color=line_color)
    pyplot.legend()

    for peak in signal_peaks_array:
        pyplot.axvline(x=peak, color=COLOR_GRAY, alpha=0.8, label=PEAK_LABEL, linestyle=LINESTYLE_DASHED)

        if (signal_peaks_array.index(peak) == 0):
            pyplot.legend() # To only print one legend

    pyplot.show()

def testCutoffFrequencies(noisy_signal, signal_sampling_rate, start_number, end_number, number_of_samples, level_of_detail=10, band_to_test=LOWPASS, stable_cutoff_frequency=0.5, show_rationale=False):
    def getClosestPerfectGrid(number):
        for i in range(2, 40): # 40 is just a limit to prevent infinite loop
            current_perfect_grid = i * i 

            if (number <= current_perfect_grid): # Then the number fits in this grid
                next_smaller_grid = i * (i - 1)

                if (number <= next_smaller_grid): # Does it fit in the previous grid?
                    return i, i - 1
                else:
                    return i, i

    def getCriticalFrequencyOrder(filter_type, stable_cutoff, variable_cutoff):
        if (filter_type == LOWPASS):
            return [stable_cutoff, variable_cutoff]

        elif (filter_type == HIGHPASS):
            return [variable_cutoff, stable_cutoff]

        else:
            print(INVALID_FILTER_TYPE_ERROR.format(filter_type))
            exit()

    noisy_signal = noisy_signal[:(len(noisy_signal) // level_of_detail)]

    stable_cutoff = stable_cutoff_frequency / (signal_sampling_rate / 2)
    variable_cutoff = 0
    steps = (end_number - start_number) / (number_of_samples - 1) # Number of steps between the tested values
    sampling_array = numpy.linspace(start_number, end_number, num=number_of_samples) # Decimal array with all values with steps
    number_of_columns, number_of_rows = getClosestPerfectGrid(number_of_samples)

    pyplot.figure(TEST_SAMPLES_TITLE.format(band_to_test))
    axis = pyplot.subplot(number_of_rows, number_of_columns, 1)

    for sample in sampling_array:
        rounded_sample = round(sample, 2)
        variable_cutoff = sample / (signal_sampling_rate / 2)
        critical_frequencies = getCriticalFrequencyOrder(band_to_test, stable_cutoff, variable_cutoff)
        b, a = signal.butter(4, critical_frequencies, BANDPASS)
        filtered_signal = signal.filtfilt(b, a, noisy_signal)
        plot_index = round((sample / steps) - ((start_number / steps) - 1))
        
        axis = pyplot.subplot(number_of_rows, number_of_columns, plot_index, xticks=[], yticks=[], sharex=axis)
        pyplot.subplots_adjust(left=0.01, bottom=0.01, right=.99, top=.99, wspace=0.05, hspace=0.05) # Reduce margins
        pyplot.plot(filtered_signal, label=TEST_FRECUENCY_TITLE.format(rounded_sample), color=COLOR_BLACK)
        pyplot.legend()

    if show_rationale: displayPopUp(CUTOFF_FREQUENCY_TEST_RATIONALE)
    pyplot.show()

def animatePlot(plot_figure, plot_axis, signal_array, x_viewing_window=500, y_viewing_window=None, y_label=None, y_label_color="blue", y_label_font_size=14, center_viewing_window_at=0, follow_height=False, follow_height_buffer=None, level_of_compression=3, hide_ticks=False, line_color="blue", show_plot=True):
    x_values, y_values = [], []

    frames_array = numpy.arange(0, len(signal_array), level_of_compression)
    last_frames_array_index = frames_array[-1]

    follow_height_buffer = follow_height_buffer if follow_height_buffer is not None else numpy.average(numpy.absolute(signal_array)) // 2

    def followPlotHeight(current_frame, axis, signal_array, x_viewing_window, follow_height_buffer):
        x_limit_value = x_viewing_window >> 1
        first_visible_frame = current_frame - x_limit_value if current_frame > x_limit_value else 0; current_frame += 2 # +2 to avoid ValueError

        maximum_value = numpy.max(signal_array[first_visible_frame : current_frame]) + follow_height_buffer
        minimum_value = numpy.min(signal_array[first_visible_frame : current_frame]) - follow_height_buffer

        axis.set_ylim(minimum_value, maximum_value)

    def constantPlotHeight(axis, y_viewing_window):
        y_limit_value = y_viewing_window >> 1

        minimum_value = -(y_limit_value) + center_viewing_window_at
        maximum_value = y_limit_value + center_viewing_window_at

        axis.set_ylim(minimum_value, maximum_value)

    def followPlotLength(current_frame, axis, x_viewing_window):
        x_limit_value = x_viewing_window >> 1

        maximum_value = current_frame + x_limit_value
        minimum_value = current_frame - x_limit_value

        if current_frame < x_limit_value:
            maximum_value = x_viewing_window
            minimum_value = 0

        elif maximum_value > last_frames_array_index: 
            maximum_value = last_frames_array_index + 1 # +1 only to show last value on x
            minimum_value = last_frames_array_index - x_viewing_window

        axis.set_xlim(minimum_value, maximum_value)

    def setPlotViewingWindow(frame, axis, signal_array, x_viewing_window, y_viewing_window, follow_height, follow_height_buffer):
        followPlotLength(frame, axis, x_viewing_window)

        if follow_height:
            followPlotHeight(frame, axis, signal_array, x_viewing_window, follow_height_buffer)

        elif y_viewing_window is not None: 
            constantPlotHeight(axis, y_viewing_window)

    def updateAnimation(frame):
        if not pyplot.fignum_exists(plot_figure.number):
            return 

        x_values.append(frame)
        y_values.append(signal_array[frame])

        pyplot.cla() # Clear current axes

        if hide_ticks:
            pyplot.xticks([])
            pyplot.yticks([])

        if y_label is not None:
            pyplot.ylabel(y_label, color=y_label_color, fontsize=y_label_font_size)

        pyplot.plot(x_values, y_values, color=line_color)

        setPlotViewingWindow(frame, plot_axis, signal_array, x_viewing_window, y_viewing_window, follow_height, follow_height_buffer) # Global variables :(

    animation_object = FuncAnimation(plot_figure, updateAnimation, frames=frames_array, interval=1, repeat=False)
    if show_plot: pyplot.show()

    return animation_object

def checkVitals(vital_sign, normal_vital_signs, popup_message, patient_name=DEFAULT_PATIENT_NAME, popup_message_type=None):
    popup_message_type = popup_message_type if popup_message_type is not None else WARNING_POPUP_TYPE
    vital_sign_name = list(vital_sign.keys())[0]
    vital_sign_value = vital_sign[vital_sign_name]
    
    vital_sign_lower_bound, vital_sign_upper_bound = normal_vital_signs[vital_sign_name][0] , normal_vital_signs[vital_sign_name][1]
    normal_vital_sign_range = vital_sign_upper_bound - vital_sign_lower_bound
    normal_vital_sign_units = normal_vital_signs[vital_sign_name][2]

    if vital_sign_value < vital_sign_lower_bound:
        vital_sign_status = LOW_VITAL_SIGN_STATUS
        vital_sign_comparator = LESSER_THAN
        vital_sign_boundary = vital_sign_lower_bound
        vital_sign_critical_point = vital_sign_boundary - normal_vital_sign_range

        if vital_sign_value < vital_sign_critical_point:
            popup_message_type = ALERT_POPUP_TYPE
            vital_sign_status = HIGH_VITAL_SIGN_CRITICAL + vital_sign_status
            vital_sign_boundary = vital_sign_critical_point

    elif vital_sign_value > vital_sign_upper_bound:
        vital_sign_status = HIGH_VITAL_SIGN_STATUS
        vital_sign_comparator = GREATER_THAN
        vital_sign_boundary = vital_sign_upper_bound
        vital_sign_critical_point = vital_sign_boundary + normal_vital_sign_range

        if vital_sign_value > vital_sign_critical_point:
            popup_message_type = ALERT_POPUP_TYPE
            vital_sign_status = HIGH_VITAL_SIGN_CRITICAL + vital_sign_status
            vital_sign_boundary = vital_sign_critical_point

    else:
        return

    displayPopUp(popup_message.format(patient_name, vital_sign_status,vital_sign_comparator ,vital_sign_boundary, normal_vital_sign_units), message_type=popup_message_type)

# This will execte every time shared is imported
setCurrentWorkingDirectory()