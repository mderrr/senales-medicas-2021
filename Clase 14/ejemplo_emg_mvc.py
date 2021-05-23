import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal

# EMG
df = pd.read_csv('EMG.csv')
sig = df['emg (2000 Hz)']
fs = 2000

sig = sig - np.mean(sig)
sig_original = np.copy(sig)

# outliers
sig = np.where(sig > (np.mean(sig) + 10*np.std(sig)), np.mean(sig), sig)
sig = np.where(sig < (np.mean(sig) - 10*np.std(sig)), np.mean(sig), sig)

# rectificación
sig = np.abs(sig)

# Filtrado
wn = 3/(fs/2)
b,a = signal.butter(5, wn, btype='lowpass')
sig = signal.filtfilt(b,a,sig)


# EMG MVC
df = pd.read_csv('MVC_EMG.csv')
mvc = df['mvc (2000 Hz)']
fs = 2000

mvc = mvc - np.mean(mvc)
mvc_original = np.copy(mvc)
plt.plot(mvc)
plt.show()

# outliers
mvc = np.where(mvc > (np.mean(mvc) + 10*np.std(mvc)), np.mean(mvc), mvc)
mvc = np.where(mvc < (np.mean(mvc) - 10*np.std(mvc)), np.mean(mvc), mvc)

# rectificación
mvc = np.abs(mvc)

# Filtrado
wn = 3/(fs/2)
b,a = signal.butter(5, wn, btype='lowpass')
mvc = signal.filtfilt(b,a,mvc)

# Encontratr el máximo del MVC
mvc_max = np.max(mvc)
# Normalizar EMG
sig_norm = sig/mvc_max

ax1 =plt.subplot(2,1,1)
plt.plot(sig_norm)
ax2 = plt.subplot(2,1,2)
plt.plot(mvc)
plt.show()