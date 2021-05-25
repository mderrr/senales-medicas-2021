import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal

df = pd.read_csv('./Clase 13/abp3.csv')
sig = df['ABP (125 Hz)']
fs = 125

sig_original = np.copy(sig)
thres = 0.55

# outliers
sig = np.where(sig > (np.mean(sig) + 10*np.std(sig)), np.mean(sig), sig)
sig = np.where(sig < (np.mean(sig) - 10*np.std(sig)), np.mean(sig), sig)

# Filtrado
wn = 15/(fs/2)
b,a = signal.butter(3, wn, btype='lowpass')
sig = signal.filtfilt(b,a,sig)

# Algoritmo
aux = np.abs(np.diff(sig))
n = int(np.round(fs/5))
aux2 = np.zeros(len(aux))
for i in range(n,len(aux)): # integral móvil con ventana n
    aux2[i] = np.sum(aux[i-n:i])
aux2_thres= np.max(aux2)
aux3 = (aux2 > (thres*aux2_thres))*1
aux4 = np.diff(aux3)
l_izq = np.where(aux4 == 1)
l_der = np.where(aux4 == -1)
l_izq = l_izq - np.array(n/2)

# picos!
peaks = np.ones(np.size(l_izq)-1)
for i in range(0,np.size(l_izq)-1):
    ind_max = np.argmax(sig[int(l_izq[0][i]):int(l_der[0][i])])
    peaks[i] = ind_max + l_izq[0][i]
# picos como int
ind_peaks = [0 for i in range(len(peaks))]
for i in range(len(peaks)):
    ind_peaks[i] = int(peaks[i])

# visualización
plt.plot(sig)
plt.plot(ind_peaks, sig[ind_peaks], 'ro')
plt.show()