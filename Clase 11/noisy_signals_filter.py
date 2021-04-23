import numpy
import pandas
from scipy import signal
from matplotlib import pyplot

noisy_signals_csv = pandas.read_csv("./Clase 11/noisy_signals.csv")
ppg_signal = noisy_signals_csv["PPG (1000 Hz)"]
abp_signal = noisy_signals_csv["ABP (125 Hz)"]
breath_signal = noisy_signals_csv["RESP (125 Hz)"]

#ax1 =pyplot.subplot(2,1,1)
#pyplot.plot(ppg_signal)
#pyplot.show()

fs = 1000

# pasa altas
Wc = 0.5 / (fs / 2)
b, a = signal.butter(3, Wc, "highpass")
ppg_signal_filtered = signal.filtfilt(b, a, ppg_signal)

# pasa bajas
Wc = 15 / (fs / 2)
b, a = signal.butter(10, Wc, "lowpass")
ppg_signal_filtered = signal.filtfilt(b, a, ppg_signal_filtered)

#ax1 =pyplot.subplot(2,1,2)
#pyplot.plot(ppg_signal_filtered)
#pyplot.show()

# ABP

# Para no quitar nvel dc
#dc = mean(abp_signal)

ax1 =pyplot.subplot(2,1,1)

pyplot.plot(abp_signal)
#pyplot.show()

fs = 125


# pasa bajas
Wc = 15 / (fs / 2)
b, a = signal.butter(10, Wc, "lowpass")
abp_signal_filtered = signal.filtfilt(b, a, abp_signal)

#abp_signal_filtered += dc

ax1 =pyplot.subplot(2,1,2,sharex=ax1)
pyplot.plot(abp_signal_filtered)
pyplot.show()