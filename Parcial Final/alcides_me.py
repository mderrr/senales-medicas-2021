import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal

vis = 1
m = 'MG'

df = pd.read_csv('EMGs.csv')
sig = df[m]
fs = 2000

sig[0] = 0 # Fix

df = pd.read_csv('MVCs.csv')
mvc = df[m + ' (Volts)']

sig = sig - np.mean(sig)
sig_original = np.copy(sig)

if vis:
    plt.plot(sig)
    plt.show()

sig = np.where(sig > (np.mean(sig) + 10*np.std(sig)), np.mean(sig), sig) # 1 to 10
sig = np.where(sig < (np.mean(sig) - 10*np.std(sig)), np.mean(sig), sig) # 1 to 10

sig = np.abs(sig) 
b,a = signal.butter(3, 3/(fs/2), btype='lowpass') # 5 to 3
sig = signal.filtfilt(b,a,sig)

if vis:
    plt.plot(sig)
    plt.show()

sig = sig / mvc[0]
sig = sig - np.min(sig)

if vis:
    plt.plot(sig)
    plt.show()

thres = 0.03
aux3 = (sig > thres)*1
aux4 = np.diff(aux3)
l_izq = np.where(aux4 == 1)
l_der = np.where(aux4 == -1)

if vis:
    plt.plot(sig)
    plt.plot(aux3*0.2)
    plt.plot([0, len(sig)], [thres, thres], color='green', linestyle='dashed')
    plt.show()

# Solución
ind_derecho = 0
ncontracciones = 0
for i in range(0,np.size(l_izq)-1):
    # necesito garantizar que el límite izq corresponda con el der
    while (l_izq[0][i] > l_der[0][ind_derecho]):
        ind_derecho += 1

    ncontracciones += 1

print('Número total de contracciones: ' + str(ncontracciones))