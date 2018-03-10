import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

x = np.array([80, 90, 100, 120, 130, 140])
y = np.array([3.4, 3.6, 3.5, 3.3, 3.5, 3])
tck = interpolate.splrep(x, y)
xnew = np.arange(80, 140, 1)
ynew = interpolate.splev(xnew, tck)
x2 = np.array([80, 100, 120, 140])
y2 = np.array([3.4, 3.5, 3.3, 3])
tck = interpolate.splrep(x2, y2)
xnew2 = np.arange(80, 140, 1)
ynew2 = interpolate.splev(xnew2, tck)
plt.plot(x, y, xnew, ynew, xnew2, ynew2)
plt.show()
