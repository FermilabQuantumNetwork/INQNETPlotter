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
n_steps = 250
#norm = cm.colors.Normalize(vmax=zmax, vmin=zmin)
#cmap = cm.get_cmap('viridis', n_steps)
#cmap = cm.get_cmap('RdBu',n_steps)
cmap = cm.get_cmap('coolwarm',n_steps)

top = cm.get_cmap('Oranges_r', 125)
bottom = cm.get_cmap('Blues', 125)

newcolors = np.vstack((top(np.linspace(0, 1, 125)),bottom(np.linspace(0, 1, 125))))

print(newcolors)

#print(len(cmap))
#print( cm.get_cmap(cmap, len(levels) - 1))

#my_mpa = cm.get_cmap(cmap, len(levels) - 1)
#print(my_mpa(0))


fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")

##############################
#####define x-axis labels#####
##############################
labels_x = ['', r'$| e \rangle$','', r'$| \ell \rangle$']
labels_y = ['', r'$\langle e |$','', r'$\langle \ell |$']

ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel("Probability")
ax.set_xlim3d(-1.0,1.0)
ax.set_ylim3d(-1.0,1.0)
ax.set_zlim3d(-1.0,1.0)

ax.set_xticklabels(labels_x)
ax.tick_params(axis='x', which='major', labelsize=20)

ax.set_yticklabels(labels_y)
ax.tick_params(axis='y', which='major', labelsize=20)

#ax.set_zlim3d(0.0,1.0)

xpos = [-0.75, 0.25]
ypos = [-0.75, 0.25]

xpos, ypos = np.meshgrid(xpos, ypos)

xpos = xpos.flatten()
ypos = ypos.flatten()
print(xpos)
print(ypos)
zpos = np.zeros_like(xpos)

#dx = np.ones_like(xpos)
#dy = np.ones_like(ypos)
dx = np.empty(4)
dx.fill(0.5)
dy = np.empty(4)
dy.fill(0.5)
print(dy,dx)
#dz = np.linspace(0.0, 1.0, num=100)
dz = []
#n_steps = 100
step = 1.0/n_steps
bin1 = 0.95
bin2 = 0.05
bin3 = 0.25
bin4 = -0.55
for i in range(n_steps):
    #print(i)
    #print (np.array([bin1*float(i)*step,bin1*float(i)*step,bin1*float(i)*step,bin1*float(i)*step]))
    dz.append(np.array([step*bin1,step*bin2,step*bin3,step*bin4]))

#print(dz)
#print(cm.colors.to_rgb(0.1))

#print(cmap(0))
#print(dz[0])

_zpos = zpos   # the starting zpos for each bar
colors = ['r', 'b', 'g', 'y']
for i in range(n_steps):
    # (colors[i])
    ax.bar3d(xpos, ypos, _zpos, dx, dy, dz[i], color=(cmap(0.5-i*step*bin1/2.0),cmap(0.5-i*step*bin2/2.0),cmap(0.5-i*step*bin3/2.0),cmap(0.5-i*step*bin4/2.0)))
    _zpos += dz[i]    # add the height of each bar to know where to start the next
    #print(_zpos)

plt.gca().invert_xaxis()
plt.show()
