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


mean = np.mean(sig)
ls = mean + 10*np.std(sig)
li = mean - 10*np.std(sig)

print(mean)
print(ls)
print(li)

plt.plot(sig)
plt.plot([0, len(sig)], [mean, mean], color='green', linestyle='dashed')
plt.plot([0, len(sig)], [ls, ls], color='red', linestyle='dashed')
plt.plot([0, len(sig)], [li, li], color='red', linestyle='dashed')
ind = (sig > ls) | (sig < li)
sig[ind] = np.mean(sig)
plt.figure()
plt.plot(sig)
plt.show()