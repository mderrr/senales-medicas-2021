import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import math 

df = pd.read_csv('Clase 6/eeg.csv')
print(df.head(5))
#df.plot( y='Amplitude', kind = 'line')

eeg = df['Amplitude']
ecg_2 = eeg[:int(len(eeg) / 2)]
ecg_4 = eeg[:int(len(eeg) / 4)]
ecg_8 = eeg[:int(len(eeg) / 8)]
ecg_32 = eeg[:int(len(eeg) / 32)]
fs = 50    
N = len(eeg)

# FFT
X = np.fft.fft(eeg)
X = np.abs(X)


# Frequency vector
f = (fs)*(np.arange(1,N+1)/N)
plt.plot(f,X)
#plt.show()
X4 = np.abs(np.fft.fft(ecg_2))
f4 = (fs)*(np.arange(1,len(ecg_2)+1)/len(ecg_2))
plt.figure("X4")
plt.plot(f4,X4)

X5 = np.abs(np.fft.fft(ecg_4))
f5 = (fs)*(np.arange(1,len(ecg_4)+1)/len(ecg_4))
plt.figure("X5")
plt.plot(f5,X5)

X6 = np.abs(np.fft.fft(ecg_8))
f6 = (fs)*(np.arange(1,len(ecg_8)+1)/len(ecg_8))
plt.figure("X6")
plt.plot(f6,X6)


X7 = np.abs(np.fft.fft(ecg_32))
f7 = (fs)*(np.arange(1,len(ecg_32)+1)/len(ecg_32))
plt.figure("X7")
plt.plot(f7,X7)

# Frequency vector (half!)
N2 = np.round(N/2)
f2 = (fs/2)*(np.arange(1,N2+1)/N2)
X2 = X[0:int(N2)]
print("ORI", N)
print("SIZEEEEEEEEEEEEE", len(f2))
plt.figure()
plt.plot(f2,X2)
plt.show()
