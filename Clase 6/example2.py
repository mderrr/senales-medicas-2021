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
sig[0:int(N / 2)] = t[0:int(N / 2)]

# Fourier decomposition
a0 = 2*np.mean(sig)
print(a0)
f = np.zeros(round(N/2))
X_mag = np.zeros(round(N/2)) 
X_phase = np.zeros(round(N/2))     
for m in range(1,3):
    f[m] = m*f1
    a = (2/N)*np.sum(sig*(np.cos(2*np.pi*f[m]*t)))
    b = (2/N)*np.sum(sig*(np.sin(2*np.pi*f[m]*t)))
    X_mag[m] = np.sqrt((a**2) + (b**2))
    X_phase[m] = -math.atan2(b,a)

# Reconstruction
sig_r = np.zeros(N)

for m in range(1, 3):
    sig_r += X_mag[m] * np.cos(2 * np.pi * f[m] * t + X_phase[m])

sig_r += a0 / 2

# Plots
plt.figure()
plt.plot(t,sig_r)
plt.plot(t,sig, linestyle='dashed')
plt.xlabel('Time(sec)',fontsize=14)
plt.ylabel('sig(t)',fontsize=14)
plt.title('5 components reconstruction',fontsize=14)
plt.show()