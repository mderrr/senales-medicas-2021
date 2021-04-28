import shared
import lab3_2a_santih

BAND_RATIO_TITLE = "Porcentaje de relación entre las bandas y la señal:\n\n"
BAND_RATIO_FORMAT = "{}:{}{}%\n"

POINT_2C_RESPONSE = "\nVisualizando estos resultados, vemos que las bandas Gamma, Theta y Beta tienen una baja relación al RMS completo, mientras que Alpha y Delta tienen una contribución mas grande, yo creo que esto significa que el paciente puede tener tendencias a TDAH, depresión, soñar despierto, ansiedad, poca conciencia emocional y estrés."

ZOOM_IN_SECONDS = 2
BAND_RATIO_NUMBER_OF_SPACES = 15

def showBandRatios(sorted_band_list):
    message = BAND_RATIO_TITLE

    for index in range(len(sorted_band_list) - 1):
        band_name, band_value = sorted_band_list[index]
        band_ratio = (band_value / sorted_band_list[-1][1]) * 100

        number_of_spaces = BAND_RATIO_NUMBER_OF_SPACES - len(band_name)
        spaces = " " * number_of_spaces

        message += BAND_RATIO_FORMAT.format(band_name, spaces, round(band_ratio, 2))

    return message

@shared.presentPoint
def main():
    noisy_eeg_signal = shared.getSignalFromFile(shared.EEG_FILE_NAME)

    rms_list = lab3_2a_santih.splitEegBands(noisy_eeg_signal, shared.EEG_SAMPLING_FREQUENCY, shared.getEegBandsList(), display_rms=True, zoom_in_seconds=ZOOM_IN_SECONDS)
    sorted_rms_list = sorted(rms_list, key=lambda band: band[1])

    band_ratios_message = showBandRatios(sorted_rms_list)

    full_response = band_ratios_message + POINT_2C_RESPONSE
    shared.displayResponse(full_response)

if __name__ == "__main__":
    main()