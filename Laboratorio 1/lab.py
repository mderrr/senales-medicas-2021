import serial
import numpy as np
import matplotlib.pyplot as plt

signal = np.ones((1000,1))

ser = serial.Serial("/dev/ttyACM0", baudrate = 115200, timeout=10)

for x in range(1000):
    try:
        dat = int(ser.readline())

    except:
        dat = 0

    signal[x] = dat

    print(signal[x])

plt.plot(signal)
plt.show()

print(signal)
ser.close()