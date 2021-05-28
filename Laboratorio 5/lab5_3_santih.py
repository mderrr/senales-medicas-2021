import numpy
from matplotlib import pyplot
import lab5_shared_santih as shared

ECG_FILE_PATH                 = "./ecg_ebeats.csv"
RESPONSE_MESSAGE              = "El paciente presenta un total de {} latidos ectópicos."
PEAKS_LABEL                   = "R Peaks"
ECTOPIC_BEATS_LABEL           = "Detected Ectopic Beats"

ECG_SAMPLING_FREQUENCY        = 125
STANDARD_DEVIATION_MULTIPLIER = 1

@shared.presentPoint
def main():
    signal              = shared.getSignalFromFile(ECG_FILE_PATH)

    peaks_array         = shared.extractPeaksFromSignal(signal)
    beat_durations      = shared.getPeakPeriods(peaks_array, ECG_SAMPLING_FREQUENCY)
    mean_beat_duration  = numpy.mean(beat_durations)

    standard_deviation  = numpy.std(signal) * STANDARD_DEVIATION_MULTIPLIER
    lower_limit         = mean_beat_duration - standard_deviation
    upper_limit         = mean_beat_duration + standard_deviation

    ectopic_beats_array = [ peaks_array[i] for i, interval in enumerate(beat_durations) if not (lower_limit < interval < upper_limit) ]

    ectopic_beats       = len(ectopic_beats_array) // 2

    print(RESPONSE_MESSAGE.format( ectopic_beats ))

    pyplot.plot(signal)
    pyplot.plot(peaks_array, signal[peaks_array], shared.BLUE_OBJECT, label=PEAKS_LABEL)
    pyplot.plot(ectopic_beats_array, signal[ectopic_beats_array], shared.RED_OBJECT, label=ECTOPIC_BEATS_LABEL)
    pyplot.legend()
    pyplot.show()

if __name__ == "__main__":
    main()