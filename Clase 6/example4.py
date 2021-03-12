import numpy as np
import matplotlib.pyplot as plt 
import math 

fs = 500          
Tt = 1            
N = Tt*fs          
f1 = 1/Tt     
t = np.arange(1,N+1)/fs 

# Construct waveform 
sig = np.zeros(N)
sig[0:int(N/2)] = t[0:int(N/2)]
plt.plot(t,sig)

# FFT
X = np.fft.fft(sig)
#X = np.abs(X)

# Reconstruction (ifft)
aux_index = np.arange(5,N-4)
X[aux_index] = 0 + 0j
sig_r = np.fft.ifft(X)
sig_r = np.real(sig_r)

plt.figure()
plt.plot(t,sig_r)
plt.plot(t,sig, linestyle='dashed')
plt.xlabel('Time(sec)',fontsize=14)
plt.ylabel('x(t)',fontsize=14)
plt.title('5 components reconstruction',fontsize=14)
plt.show()