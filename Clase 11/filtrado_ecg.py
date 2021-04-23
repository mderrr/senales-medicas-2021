import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt 

df = pd.read_csv("./Clase 11/ecg_noisy2.csv")
ecg = df["ECG1000"]
fs = 1000
N = len(ecg)

# plt.plot(ecg)

# # FFT
X = np.fft.fft(ecg)
X = np.abs(X)
f = (fs)*(np.arange(1,N+1)/N)
# plt.figure()
# plt.plot(f,X)
# plt.xlim((0, fs/2))

# # Filtro pasa altas
Wc = 0.2/(fs/2)
b, a = signal.butter(5, Wc, "highpass")
ecg_f = signal.filtfilt(b, a, ecg)
print(a)
print(b)
plt.figure()
plt.plot(ecg)
plt.plot(ecg_f)

# # Filtro pasa bajas
Wc = 50/(fs/2)
b, a = signal.butter(10, Wc, "lowpass")
ecg_f2 = signal.filtfilt(b, a, ecg_f)

plt.figure()
plt.plot(ecg_f)
plt.plot(ecg_f2)
plt.show()