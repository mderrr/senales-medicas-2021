from matplotlib import pyplot
import lab5_shared_santih as shared

EMG_FILE_PATH        = "./emg_lesion.csv"
EMG_FIGURE_TITLE     = "EMG Signal"
EMGS_FIGURE_TITLE    = "EMG Signals"
EMG_FIGURE_SUPTITLE  = "Plotted EMG signals"
EMGS_FIGURE_SUPTITLE = "EMG Signals"
SIGNAL_LABEL_FORMAT  = "Signal {}"
DAY_KEY_FORMAT       = "DIA {}"

DAYS_ARRAY           = [0, 5, 15, 20, 30]

@shared.presentPoint
def main():
    emg_signals = [shared.getSignalFromFile(EMG_FILE_PATH, DAY_KEY_FORMAT.format(i)) for i in DAYS_ARRAY]

    pyplot.figure(EMG_FIGURE_TITLE)
    pyplot.suptitle(EMG_FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    for i, signal in enumerate(emg_signals):
        pyplot.plot(signal, alpha=0.5, label=SIGNAL_LABEL_FORMAT.format(i + 1))
        pyplot.ylim(-5, 5)

    pyplot.legend()
    pyplot.show()
    
    pyplot.figure(EMGS_FIGURE_TITLE)
    pyplot.suptitle(EMGS_FIGURE_SUPTITLE, fontsize=shared.SUPTITLE_FONT_SIZE)

    for i in range(len(DAYS_ARRAY)):
        pyplot.subplot(2, 3, i + 1).plot(emg_signals[i])
        pyplot.ylim(-5, 5)

    pyplot.show()

if __name__ == "__main__":
    main()