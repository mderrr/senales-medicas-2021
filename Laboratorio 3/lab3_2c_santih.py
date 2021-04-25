import shared
from lab3_2a_santih import splitEegBands

POINT_TITLE = "Punto 2c"
EEG_SIGNAL_FILE = "eeg_1min.csv"
ZOOM_IN_SECONDS = 2
BAND_RATIO_TITLE = "\nPorcentaje de relación entre las bandas y la señal completa:"
BAND_RATIO_FORMAT = "{}:\t{}%"
POINT_2C_RESPONSE = ("\nRESPUESTA 2C: Visualizando estos resultados, vemos que las bandas Gamma, Theta y Beta tienen una baja relacion al RMS completo, "
                    "mientras que Alpha y Delta tienen una contribucion mas grande, yo creo que esto significa que el paciente puede tener tendencias a "
                    "TDAH, depresion, soñar despierto, ansiedad, poca conciencia emocional y estres.")

noisy_eeg_signal = shared.getSignalFromFile(EEG_SIGNAL_FILE)

def showBandRatios(sorted_band_list):
    print(BAND_RATIO_TITLE)

    for index in range(len(sorted_band_list) - 1):
        name, value = sorted_band_list[index]
        ratio = (value / sorted_band_list[-1][1]) * 100

        print(BAND_RATIO_FORMAT.format(name, round(ratio, 2)))

shared.clear(POINT_TITLE)

rms_list = splitEegBands(shared.EEG_BANDS_LIST, noisy_eeg_signal, display_rms=True, zoom_in_seconds=ZOOM_IN_SECONDS)
sorted_rms_list = sorted(rms_list, key=lambda band: band[1])

showBandRatios(sorted_rms_list)
print(POINT_2C_RESPONSE)