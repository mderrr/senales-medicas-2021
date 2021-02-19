# Cargar una señal de un archivo .csv y graficarla

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

df = pd.read_csv('PPG1.csv')
print(df)
print(df.columns)
df.plot( y=df.columns, kind = 'line', subplots=True)

from my_snr import my_snr
signal = df['Anular filtered']
noise = df['Anular'] - signal
plt.figure()
plt.plot(noise)
snr_out = my_snr(signal, noise)
print("SNR is " , np.round(snr_out,2))
plt.show()

