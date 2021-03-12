import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import math 

df = pd.read_csv('eeg.csv')
print(df.head(5))
#df.plot( y='Amplitude', kind = 'line')

eeg = df['Amplitude']
fs = 50    
N = len(eeg)

# FFT
X = np.fft.fft(eeg)
X = np.abs(X)

# Frequency vector
f = (fs)*(np.arange(1,N+1)/N)
plt.plot(f,X)
#plt.show()

# Frequency vector (half!)
N2 = np.round(N/2)
f2 = (fs/2)*(np.arange(1,N2+1)/N2)
X2 = X[0:int(N2)]
plt.figure()
plt.plot(f2,X2)
plt.show()
