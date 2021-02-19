def my_snr(signal, noise):
    import math
    aux_s = (signal**2).sum()
    rms_signal = math.sqrt(aux_s/len(signal))
    aux_n = (noise**2).sum()
    rms_noise = math.sqrt(aux_n/len(noise))
    snr_out = 20 * math.log10(rms_signal/rms_noise)
    return snr_out