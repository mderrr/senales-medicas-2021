import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal

df = pd.read_csv('./Clase 14/EMG.csv')
sig = df['emg (2000 Hz)']
fs = 2000

sig = sig - np.mean(sig)
sig_original = np.copy(sig)
plt.plot(sig_original)
plt.show()

# outliers
sig = np.where(sig > (np.mean(sig) + 10*np.std(sig)), np.mean(sig), sig)
sig = np.where(sig < (np.mean(sig) - 10*np.std(sig)), np.mean(sig), sig)

# rectificación
sig = np.abs(sig)

# Filtrado
wn = 3/(fs/2)
b,a = signal.butter(5, wn, btype='lowpass')
sig = signal.filtfilt(b,a,sig)
ax1 =plt.subplot(2,1,1)
plt.plot(sig_original)
ax2 = plt.subplot(2,1,2,sharex=ax1)
plt.plot(sig)
plt.show()
