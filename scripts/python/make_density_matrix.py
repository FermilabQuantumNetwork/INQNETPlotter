import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize
from matplotlib import cm
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import os
import time


#xAmplitudes = np.random.exponential(10,10000) #your data here
#yAmplitudes = np.random.normal(50,10,10000) #your other data here - must be same array length
zmax = 1.01
zmin = 0.0
#levels = np.arange(zmin, zmax, 0.4)
#print(levels)
# Boost the upper limit to avoid truncation errors.
norm = cm.colors.Normalize(vmax=zmax, vmin=zmin)
cmap = cm.PRGn

#print( cm.get_cmap(cmap, len(levels) - 1))

#my_mpa = cm.get_cmap(cmap, len(levels) - 1)
#print(my_mpa(0))


fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_xlim3d(0,10)
ax.set_ylim3d(0,10)

xpos = [2,5,8,2,5,8,2,5,8]
ypos = [1,1,1,5,5,5,9,9,9]
zpos = np.zeros(9)

dx = np.ones(9)
dy = np.ones(9)
dz = [np.random.random(9) for i in range(200)]  # the heights of the 4 bar sets

print(dz)
#print(cm.colors.to_rgb(0.1))

_zpos = zpos   # the starting zpos for each bar
colors = ['r', 'b', 'g', 'y']
for i in range(200):
    # (colors[i])
    ax.bar3d(xpos, ypos, _zpos, dx, dy, dz[i], color=cmap(i))
    _zpos += dz[i]    # add the height of each bar to know where to start the next

plt.gca().invert_xaxis()
plt.show()
