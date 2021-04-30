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


sig_copy = np.copy(sig)

ind = np.where(sig_copy==0)
print(ind)