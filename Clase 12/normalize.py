import numpy as np
import matplotlib.pyplot as plt 
import os
import pandas

CURRENT_FILE_DIRECTORY = os.path.dirname(__file__)

if (CURRENT_FILE_DIRECTORY != os.getcwd()):
    os.chdir(CURRENT_FILE_DIRECTORY)



sig = pandas.read_csv("./outlier_ecg.csv")
sig = sig[list(sig.keys())[0]]
plt.plot(sig)


#sig = np.random.randint(10,100,20)


plt.subplot(2,1,1)
plt.plot(sig)
plt.title('Señal original')
plt.grid()



sig = sig - np.min(sig)
sig = sig / np.max(sig)
plt.subplot(2,1,2)
plt.plot(sig)
plt.title('Señal normalizada')
plt.grid()

plt.show()