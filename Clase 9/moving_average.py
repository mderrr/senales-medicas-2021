import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

df = pd.read_csv('./Clase 9/ecg_noisy.csv')
ecg1 = df['ECG1000']
ecg1 = ecg1 - np.mean(ecg1)
N = len(ecg1)
fs = 1000

plt.subplot(2,2,1)
plt.plot(ecg1)
window = 15
ecg_avg = np.zeros(N)
for i in range(N-window):
    ecg_avg[i+window] = np.mean(ecg1[i:i+window])

plt.subplot(2,2,3)
plt.plot(ecg_avg)

plt.subplot(2,2,2)
X = np.fft.fft(ecg1)
X = np.abs(X)
f = (fs)*(np.arange(1,N+1)/N)
plt.plot(f,X)
plt.xlim((0, fs/2))

plt.subplot(2,2,4)
X = np.fft.fft(ecg_avg)
X = np.abs(X)
f = (fs)*(np.arange(1,N+1)/N)
plt.plot(f,X)
plt.xlim((0, fs/2))
plt.show()