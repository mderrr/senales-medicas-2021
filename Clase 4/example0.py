import numpy as np
import matplotlib.pyplot as plt 

a = [3, 4, 5, 4, 3, 0, -1,-5, -2, 2]
b = [3.2, 2.8, 6, 3, 3.4, 0.5, -1.5, -5.2, -2.4, 1]
c = [4, 5, 2, 3, 1, 2, 4, 3, 1, 3]
d = [0, -1, -2, -5, -6, -2, 4, 4, 4, 2]

a = a - np.mean(a)
b = b - np.mean(b)
c = c - np.mean(c)
d = d - np.mean(d)

print(b)

ax1 = plt.subplot(131)
plt.plot(a)
plt.plot(b)
plt.title('sum (sig1 * sig2) = ' +  str(round(np.sum(a*b),2)), fontsize=20)
plt.grid()
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
ax1 = plt.subplot(132)
plt.plot(a)
plt.plot(c)
plt.title('sum (sig1 * sig3) = ' +  str(round(np.sum(a*c),2)), fontsize=20)
plt.grid()
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
ax1 = plt.subplot(133)
plt.plot(a)
plt.plot(d)
plt.title('sum (sig1 * sig4) = ' +  str(round(np.sum(a*d),2)), fontsize=20)
plt.grid()
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()
