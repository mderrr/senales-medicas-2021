import numpy
from matplotlib import pyplot
import lab5_shared_santih as shared

EMG_FILE_PATH         = "./emg_lesion.csv"
MVCS_FILE_PATH        = "./MVCs.csv"
DAY_KEY_FORMAT        = "DIA {}"
FIGURE_TITLE          = "Strength"
FIGURE_SUPTITLE       = "Plot of patient's strength"
X_LABEL               = "Day"
Y_LABEL               = "Strength (%)"
PEAK_LABEL            = "Peaks"
DEFAULT_CONVOLVE_MODE = "same"

DAYS_ARRAY            = [0, 5, 15, 20, 30]

@shared.presentPoint
def main():
    emg_signals = [ shared.getSignalFromFile(EMG_FILE_PATH, DAY_KEY_FORMAT.format(i)) for i in DAYS_ARRAY ]
    mvc_signals = [ list(shared.getSignalFromFile(MVCS_FILE_PATH, DAY_KEY_FORMAT.format(i)))[0] for i in DAYS_ARRAY ]
    
    percentages = [ round( (max(emg_signals[i]) / mvc_signals[i]) * 100 ) for i in range(len(DAYS_ARRAY)) ]

    pyplot.figure(FIGURE_TITLE)
    pyplot.suptitle(FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)
    pyplot.plot(DAYS_ARRAY, percentages)
    pyplot.plot(DAYS_ARRAY, percentages, shared.BLUE_OBJECT, label=PEAK_LABEL)
    pyplot.xlabel(X_LABEL)
    pyplot.ylabel(Y_LABEL)
    pyplot.show()

if __name__ == "__main__":
    main()