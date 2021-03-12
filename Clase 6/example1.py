import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import math 

df = pd.read_csv("./Clase 6/eeg.csv")
print(df.head(5))            

eeg = df["Amplitude"]
fs = 50
N = len(eeg)
Tt = N / fs
f1 = 1 / Tt
t = (np.arange(0, len(eeg)) - 1) / fs
f = np.zeros(round(N / 2))
X_mag = np.zeros(round(N / 2))
X_phase = np.zeros(round(N / 2))

for m in range(1, round(N / 2)):
    f[m] = m * f1
    a = np.sum(eeg * np.cos(2 * np.pi * f[m] * t))
    b = np.sum(eeg * np.sin(2 * np.pi * f[m] * t))
    X_mag[m] = np.sqrt((a**2) + (b**2))
    X_phase[m] = math.atan2(b, a)

X_phase *= 360
X_phase /= 2 * np.pi

# Plots
ax = plt.subplot(2,1,1)
plt.plot(f,X_mag)              
plt.xlabel('Frequency (Hz)',fontsize= 14)
plt.ylabel('|X(m)|',fontsize= 14)
ax = plt.subplot(2,1,2)
plt.plot(f,X_phase)              
plt.xlabel('Frequency (Hz)',fontsize= 14)
plt.ylabel('Phase (deg)',fontsize= 14)
plt.figure()
plt.plot(eeg)
plt.show()