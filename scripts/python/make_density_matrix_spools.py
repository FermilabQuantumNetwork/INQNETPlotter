import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import os
import time


zmax = 0.1#max z-scale
zmin = 0.0
norm = cm.colors.Normalize(vmax=zmax, vmin=-zmax)

#levels = np.arange(zmin, zmax, 0.4)
#print(levels)
# Boost the upper limit to avoid truncation errors.
n_steps = 250
#norm=cm.colors.LogNorm(vmin=-zmax, vmax=zmax)
#cmap = cm.get_cmap('viridis', n_steps)
#cmap = cm.get_cmap('RdBu',n_steps)
cmap = cm.get_cmap('coolwarm',n_steps)
print(cmap(1))
#nodes = [0.0, 0.4, 0.8, 1.0]
#cmap2 = cmap.from_list("mycmap", list(zip(nodes, colors)))
#norm=cmap.colors.LogNorm(vmin=zmin, vmax=zmax)
#norm=cm.colors.LogNorm(vmin=zmin, vmax=zmax)

top = cm.get_cmap('Oranges_r', 125)
bottom = cm.get_cmap('Blues', 125)

newcolors = np.vstack((top(np.linspace(0, 1, 125)),bottom(np.linspace(0, 1, 125))))



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

#mapping is [ee, le, el, ll]
#early-teleportation
#bin = [0.014, 0.035 , 0.035, 0.986]#Re-part early teleportation
#bin = np.array([0.0, 0.009 , -0.009, 0.0])#Im-part early teleportation
#late-teleportation
#bin = [0.962,-0.056,-0.056,0.038]#Re-part late teleportation
#bin = [0.0,-0.042,0.042,0.0]#Im-part late teleportation
#plus-teleportation
#bin = [0.515,0.331,0.331,0.485]#Re-part plus teleportation
bin = [0.0,0.029,-0.029,0.0]#Im-part plus teleportation


fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
##############################
#####define x-axis labels#####
##############################
labels_x = ['', r'$| e \rangle$','', r'$| \ell \rangle$']
labels_y = ['', r'$\langle e |$','', r'$\langle \ell |$']
labels_z = [str(-zmax), '', '0.0',  '', str(zmax)]

ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel("Amplitude")
ax.set_xlim3d(-1.0,1.0)
ax.set_ylim3d(-1.0,1.0)
ax.set_zlim3d(-zmax,zmax)

ax.set_xticklabels(labels_x)
ax.tick_params(axis='x', which='major', labelsize=20)

ax.set_yticklabels(labels_y)
ax.tick_params(axis='y', which='major', labelsize=20)

ax.set_zticklabels(labels_z)
ax.tick_params(axis='z', which='major', labelsize=15)


scale_factor = 1.0/zmax
print ('scale_factor: ', scale_factor)
color_dic = []
for i in range(n_steps):
    #print(i)
    #print (np.array([bin1*float(i)*step,bin1*float(i)*step,bin1*float(i)*step,bin1*float(i)*step]))
    dz.append(np.array([step*bin[0],step*bin[1],step*bin[2],step*bin[3]]))
    color_dic.append(np.array([cmap(0.5+scale_factor*i*step*bin[0]/2.0),
        cmap(0.5+scale_factor*i*step*bin[1]/2.0),
        cmap(0.5+scale_factor*i*step*bin[2]/2.0),
        cmap(0.5+scale_factor*i*step*bin[3]/2.0)]))

#print(dz)
#print(cm.colors.to_rgb(0.1))

#print(cmap(0))
#print(dz[0])

_zpos = zpos   # the starting zpos for each bar
colors = ['r', 'b', 'g', 'y']
for i in range(n_steps):
    # (colors[i])
    #print(0.5-i*step*bin1/2.0,cmap(0.5-i*step*bin1/2.0))
    pcb = ax.bar3d(xpos, ypos, _zpos, dx, dy, dz[i], color=color_dic[i])
    #ax.bar3d(xpos, ypos, _zpos, dx, dy, dz[i], norm=cm.colors.Normalize(vmin=zmin, vmax=zmax), cmap="coolwarm")
    _zpos += dz[i]    # add the height of each bar to know where to start the next
    #print(_zpos)

#fig.colorbar(pcb, ax=ax)

ax.zaxis.set_label_coords(0.4, 0.5)
#cbaxes = fig.add_axes([0.1, 0.1, 0.03, 0.8
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
#ax.yaxis.set_ticks_position(position='left')
#plt.gca().invert_xaxis()
plt.show()
