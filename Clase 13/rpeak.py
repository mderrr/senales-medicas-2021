import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df = pd.read_csv('./Clase 13/ecg7.csv')
sig = df['ECG (1000 Hz)']
fs = 1000

sig_original = np.copy(sig)
threshold = 0.5
# outliers
sig = np.where(sig > (np.mean(sig) + 10*np.std(sig)), np.mean(sig), sig)
sig = np.where(sig < (np.mean(sig) - 10*np.std(sig)), np.mean(sig), sig)
# Filtrado
wn1 = 1/(fs/2)
wn2 = 40/(fs/2)
b,a = signal.butter(3, [wn1, wn2], btype='bandpass')
sig = signal.filtfilt(b,a,sig)
# Normalizo
sig = sig - np.min(sig)
sig = sig / np.max(sig)
ax1 = plt.subplot(3,1,1)
plt.plot(sig)
plt.show(block=False)
# Algoritmo
aux = np.abs(np.diff(sig))
plt.subplot(3,1,2, sharex=ax1)
plt.plot(aux)
plt.show(block=False)
n = int(np.round(fs/20))
aux2 = np.zeros(len(aux))
for i in range(n,len(aux)): # integral móvil con ventana n
    aux2[i] = np.sum(aux[i-n:i])
plt.subplot(3,1,3, sharex=ax1)
plt.plot(aux2)
plt.show(block=False)
aux2_thres= np.max(aux2)
aux3 = (aux2 > (threshold*aux2_thres))*1
plt.figure()
plt.plot(sig)
plt.plot(aux3)
plt.show(block=False)
aux4 = np.diff(aux3)
# plt.figure()
# plt.plot(aux4)
# plt.show(block=False)
l_izq = np.where(aux4 == 1)
l_der = np.where(aux4 == -1)
l_izq = l_izq - np.array(n)

# picos!
peaks = np.ones(np.size(l_izq)-1)
print(peaks)
for i in range(0,np.size(l_izq)-1):
    ind_max = np.argmax(sig[int(l_izq[0][i]):int(l_der[0][i])])
    peaks[i] = ind_max + l_izq[0][i]
# picos como int
ind_peaks = [0 for i in range(len(peaks))]
for i in range(len(peaks)):
    ind_peaks[i] = int(peaks[i])

# visualización
plt.figure()
plt.plot(sig)
print(peaks)
plt.plot(ind_peaks, sig[ind_peaks], 'ro')
plt.show()
