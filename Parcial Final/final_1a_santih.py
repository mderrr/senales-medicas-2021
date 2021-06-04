from matplotlib import pyplot
import numpy
from scipy.signal.filter_design import normalize
import final_shared_santih as shared

ECG_FILE_PATH                 = "./ecg.csv"
RESPONSE_MESSAGE              = "El paciente presenta un total de {} latidos ectópicos."
PEAKS_LABEL                   = "R Peaks"
ECTOPIC_BEATS_LABEL           = "Detected Ectopic Beats"

ECG_SAMPLING_FREQUENCY        = 1000
STANDARD_DEVIATION_MULTIPLIER = 1/20_000

@shared.presentPoint
def main():
    
    signal              = shared.getSignalFromFile(ECG_FILE_PATH)

    filtered_signal     = shared.getFilteredSignal(signal, ECG_SAMPLING_FREQUENCY)

    peaks_array         = shared.extractPeaksFromSignal(filtered_signal, prominence_factor=10_000)

    beat_durations      = shared.getPeakPeriods(peaks_array, ECG_SAMPLING_FREQUENCY)
    mean_beat_duration  = numpy.mean(beat_durations)

    standard_deviation  = numpy.std(filtered_signal) * STANDARD_DEVIATION_MULTIPLIER
    lower_limit         = mean_beat_duration - standard_deviation
    upper_limit         = mean_beat_duration + standard_deviation

    ectopic_beats_array = [ peaks_array[i] for i, interval in enumerate(beat_durations) if not (lower_limit < interval < upper_limit) ]

    ectopic_beats       = len(ectopic_beats_array)

    print(RESPONSE_MESSAGE.format( ectopic_beats ))

    pyplot.plot(filtered_signal)
    pyplot.plot(peaks_array, filtered_signal[peaks_array], shared.BLUE_OBJECT, label=PEAKS_LABEL)
    pyplot.plot(ectopic_beats_array, filtered_signal[ectopic_beats_array], shared.RED_OBJECT, label=ECTOPIC_BEATS_LABEL)
    pyplot.legend()
    pyplot.show()

    only_normal_peaks_array = [ peaks_array[i] for i, interval in enumerate(beat_durations) if (lower_limit < interval < upper_limit) ]

    full_heart_rate = shared.getPeakRate(peaks_array, ECG_SAMPLING_FREQUENCY)
    only_normal_heart_rate = shared.getPeakRate(only_normal_peaks_array, ECG_SAMPLING_FREQUENCY)

    print("Si tomamos en cuenta todos los latidos de la señal el paciente tiene una frecuencia cardiaca de {} Lpm.".format(full_heart_rate))
    print("Mientras que si excluimos los latidos ectopicos tendria una fecuencia de {} Lpm.".format(only_normal_heart_rate))

if __name__ == "__main__":
    main()