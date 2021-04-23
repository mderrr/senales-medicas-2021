from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

fs = 1000
order = 10
Wc = 250/(fs/2)
print('Frecuencia de corte normalizada: ' + str(Wc))

# FIR
b = signal.firwin(order+30, Wc)
w, h = signal.freqz(b)
h = abs(h)
w = (w*fs)/(2*np.pi) # convierte radianes/muestra a frecuencia Hz

plt.plot(w,h, label='FIR')

# IIR (butterworth)
b, a = signal.butter(order, Wc)
w1, h1 = signal.freqz(b, a)
h1 = abs(h1)
w1 = (w1*fs)/(2*np.pi)

plt.plot(w1,h1, label='IIR')
plt.legend()
plt.grid()
plt.show()