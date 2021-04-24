from scipy import signal
from matplotlib import pyplot
import os, platform, pandas, numpy

CURRENT_FILE_DIRECTORY = os.path.dirname(__file__)

WINDOWS_PLATFORM_NAME = "Windows"
WINDOWS_CLEAR = "cls"
UNIX_CLEAR = "clear"

BANDPASS = "bandpass"
LOWPASS = "lowpass"
HIGHPASS = "highpass"

INVALID_FILTER_TYPE_ERROR = "The argument: '{}' was not recognized, valid arguments are: 'lowpass' or 'highpass'."

TEST_SAMPLES_TITLE = "Test samples for {} band"
TEST_FRECUENCY_TITLE = "Critical frequency of ~{}Hz"

POINT_TITLE_TEMPLATE = "////////////////  {}  ////////////////\n"

def setCurrentWorkingDirectory():
    if (CURRENT_FILE_DIRECTORY != os.getcwd()):
        os.chdir(CURRENT_FILE_DIRECTORY)

def clear(title=""):
    os.system(WINDOWS_CLEAR if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_CLEAR)
    if title: print(POINT_TITLE_TEMPLATE.format(title))

def getSignalFromFile(file_name, first_key=""):
    file_dictionary = pandas.read_csv(file_name)
    if not first_key: first_key = list(file_dictionary.keys())[0]
    return file_dictionary[first_key]

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

# This will execte every time shared is imported
setCurrentWorkingDirectory()