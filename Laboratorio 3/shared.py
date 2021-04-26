from scipy import signal
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import EngFormatter as plotTickFormatter
import os, sys, platform, pandas, numpy

CURRENT_FILE_DIRECTORY = os.path.dirname(__file__)

WINDOWS_PLATFORM_NAME = "Windows"
WINDOWS_CLEAR = "cls"
UNIX_CLEAR = "clear"

BANDPASS = "bandpass"
LOWPASS = "lowpass"
HIGHPASS = "highpass"

COLOR_GRAY = "gray"
COLOR_RED = "red"
COLOR_GREEN = "green"
COLOR_ORANGE = "orange"
COLOR_BLUE = "blue"
COLOR_YELLOW = "yellow"

HERTZ = "Hz"

LINESTYLE_DASHED = "dashed"

LOW_CUTOFF_VALUE = 0.5
HIGH_CUTOFF_VALUE = 25

SUPTITLE_FONT_SIZE = 16
LABEL_FONT_SIZE = 14

INVALID_FILTER_TYPE_ERROR = "The argument: '{}' was not recognized, valid arguments are: 'lowpass' or 'highpass'."

TEST_SAMPLES_TITLE = "Test samples for {} band"
TEST_FRECUENCY_TITLE = "Critical frequency of ~{}Hz"

POINT_TITLE_TEMPLATE = "////////////////  Point {}  ////////////////"

EEG_BAND_NAMES = [
    "Original Signal",
    "Gamma: 30Hz to 100Hz+",
    "Beta: 12Hz to 30Hz", 
    "Alpha: 8Hz to 12Hz",
    "Theta: 4Hz to 7Hz", 
    "Delta: 0Hz to 4Hz"
]

def getEegBandsList(verbose=False):
    eeg_band_names = EEG_BAND_NAMES

    if not verbose:
        for i in range(len(eeg_band_names)):
            eeg_band_names[i] = eeg_band_names[i].split(":")[0]

    return [
        (0, 0, eeg_band_names[0], 1, "midnightblue"),
        (30, 0 , eeg_band_names[1], 3, "navy"),
        (12, 30 , eeg_band_names[2], 5, "darkblue"),
        (8, 12 , eeg_band_names[3], 2, "mediumblue"),
        (4, 7 , eeg_band_names[4], 4, "blue"),
        (0, 4 , eeg_band_names[5], 6, "royalblue")
    ]

def setCurrentWorkingDirectory():
    if (CURRENT_FILE_DIRECTORY != os.getcwd()):
        os.chdir(CURRENT_FILE_DIRECTORY)

def clear(title=""):
    os.system(WINDOWS_CLEAR if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_CLEAR)
    if title: print(POINT_TITLE_TEMPLATE.format(title))

def presentPoint(main_function):
    point_name = os.path.basename(sys.argv[0]).split("_")[1]
    clear(point_name)

    return main_function

def getPlotTickFormatter(units, separator=""):
    return plotTickFormatter(unit=units, sep=separator)

def getSignalFromFile(file_name, dict_key=""):
    file_dictionary = pandas.read_csv(file_name)
    if not dict_key: dict_key = list(file_dictionary.keys())[0]
    return file_dictionary[dict_key]

def getRootMeanSquare(signal):
    squared_signal = signal ** 2
    rms_value = numpy.sqrt(numpy.sum(squared_signal) / len(squared_signal))

    return rms_value

def filterSignal(noisy_signal, signal_samping_rate, low_cutoff_value=LOW_CUTOFF_VALUE, high_cutoff_value=HIGH_CUTOFF_VALUE, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0
    low_cutoff = low_cutoff_value / (signal_samping_rate / 2)
    high_cutoff = high_cutoff_value / (signal_samping_rate / 2)
    cutoff_frequencies = [low_cutoff, high_cutoff]
    b, a = signal.butter(4, cutoff_frequencies, BANDPASS)

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal

def simpleFilterSignal(noisy_signal, signal_samping_rate, filter_type, cutoff_value, acount_for_dc_level=False):
    dc_level = numpy.mean(noisy_signal) if acount_for_dc_level else 0

    cutoff = cutoff_value / (signal_samping_rate / 2)
    b, a = signal.butter(4, cutoff, filter_type)

    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    filtered_signal += dc_level

    return filtered_signal
    
def testCutoffFrequencies(noisy_signal, signal_sampling_rate, start_number, end_number, number_of_samples, band_to_test=LOWPASS, stable_cutoff_frequency=25):
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
            return [variable_cutoff, stable_cutoff]

        elif (filter_type == HIGHPASS):
            return [stable_cutoff, variable_cutoff]

        else:
            print(INVALID_FILTER_TYPE_ERROR.format(filter_type))
            exit()

    stable_cutoff = stable_cutoff_frequency / (signal_sampling_rate / 2)
    variable_cutoff = 0
    steps = (end_number - start_number) / (number_of_samples - 1) # Number of steps between the tested values
    sampling_array = numpy.linspace(start_number, end_number, num=number_of_samples) # Decimal array with all values with steps
    pyplot.figure(TEST_SAMPLES_TITLE.format(band_to_test))

    for sample in sampling_array:
        rounded_sample = round(sample, 2)
        variable_cutoff = sample / (signal_sampling_rate / 2)
        critical_frequencies = getCriticalFrequencyOrder(band_to_test, stable_cutoff, variable_cutoff)
        b, a = signal.butter(4, critical_frequencies, BANDPASS)
        filtered_signal = signal.filtfilt(b, a, noisy_signal)
        plot_index = round((sample / steps) - ((start_number / steps) - 1))
        number_of_columns, number_of_rows = getClosestPerfectGrid(number_of_samples)
        
        try:
            axis = pyplot.subplot(number_of_rows, number_of_columns, plot_index, xticks=[], yticks=[], title=TEST_FRECUENCY_TITLE.format(rounded_sample), sharex=axis)
        
        # Throws exeception on first subplot because of shared x, so remove it
        except UnboundLocalError:
            axis = pyplot.subplot(number_of_rows, number_of_columns, plot_index, xticks=[], yticks=[], title=TEST_FRECUENCY_TITLE.format(rounded_sample))

        pyplot.subplots_adjust(left=0.01, bottom=0.01, right=.99, top=.97, wspace=0.045, hspace=0.1) # Reduce margins
        pyplot.plot(filtered_signal)

    pyplot.show()

def getEegBand(noisy_signal, signal_sampling_rate, band_bounds, return_fft=False, do_not_filter=False):
    filter_type = BANDPASS
    lower_bound, higher_bound, _, _, _ = band_bounds
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
        filtered_signal_size = len(filtered_signal)
        filtered_signal -= numpy.mean(filtered_signal)
        transformed_signal = numpy.abs(numpy.fft.fft(filtered_signal))
        frequency_array = (signal_sampling_rate) * (numpy.arange(1, filtered_signal_size + 1) / filtered_signal_size)

        return frequency_array, transformed_signal

    return filtered_signal

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

# This will execte every time shared is imported
setCurrentWorkingDirectory()