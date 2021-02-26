from matplotlib import pyplot as plt
import serial
import numpy as np
import pandas as pd

Fs = 1000
t = 5   #10 segundos de grabación
signal = np.ones((Fs*t,1))

serial_com = "/dev/ttyACM0"  # seleccionar el COM adecuado
ser = serial.Serial(serial_com, baudrate = 115200, timeout=10)

for x in range(Fs*t):
        try:
            dat = int(ser.readline())

        except:
            dat = 0

        signal[x] = dat

        print(dat)

a = "A=0.05, O=0.1, F=100{}"
# Save the signal here as csv
df=pd.DataFrame(signal, columns=['Amplitude'])
df.to_csv(a.format(".csv"))

# Plot
plt.figure()
plt.plot(signal)
#plt.show()
plt.savefig(a.format(".png"), bbox_inches='tight')
ser.close()