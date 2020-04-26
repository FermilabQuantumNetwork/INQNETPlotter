import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import matplotlib.patches as mpatch
from matplotlib.lines import Line2D

#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import os
import time


##############################
#####define x-axis labels#####
##############################
labels = [r'$| e \rangle \langle e |$', r'$| e \rangle \langle  \ell |$', r'$| \ell  \rangle \langle e |$', r'$| \ell  \rangle \langle \ell |$']

######################################
#flag to determin what data to plot
#is_spools_ = True -> plot spool data
#####################################
is_spools_ = True
#define lists for plot
dsm_means = []
dsm_unc = []
qst_means = []
qst_unc = []

if is_spools_ :
    ##########################################
    #####Spools result from CQNET-March2020
    ##########################################
    print('[INFO]: plotting spool data')
    dsm_means = [0.9861, 0.9842, 0.845, 0.8917166667]#Decoy State Method (DSM) teleportation results
    dsm_unc   = [0.0088, 0.0087, 0.0332, 0.02222921626]#DSM uncertainty
    qst_means = [0.986, 0.962, 0.831, 0.8786666667]#Quamtum State Tomography (QST) teleportation results
    qst_unc   = [0.0064, 0.0186, 0.0497, 0.03329512811]#QST uncertainty
else:
    print('[INFO]: plotting no-spool data')
    ##########################################
    #####No-spools result from CQNET-March2020
    ##########################################
    dsm_means = [0.9925, 0.9792, 0.9028, 0.9304833333]#Decoy State Method (DSM) teleportation results
    dsm_unc   = [0.0058, 0.0127, 0.0589, 0.03933555432]#DSM uncertainty
    qst_means = [0.952, 0.959, 0.85, 0.8851666667]#Quamtum State Tomography (QST) teleportation results
    qst_unc   = [0.012, 0.013, 0.016, 0.01106671687]#QST uncertainty


#x = np.arange(len(labels))  # the label locations
#print(x)
#--------------------------------------
# the label locations -- equally spaced
#--------------------------------------
data_shift = 0.0
x = np.array([0.0,1.0,2.0,3])
x_mesured  = []
x_expected = []
for i in x:
    x_mesured.append(i-data_shift);
    x_expected.append(i+data_shift);

y_measured_re = np.array([0.041, -0.026 , -0.026, 0.959])
y_measured_im = np.array([0.0, 0.009 , -0.009, 0.0])
y_expected_re = np.array([0.0,0.0,0.0,1.0])
y_expected_im = np.array([0.0,0.0,0.0,0.0])

width = 0.45  # the width of the bars

#fig, ax = plt.subplots(1,1, num=304, sharex = True)
fig, ax = plt.subplots(2,1, num=304, sharex = True)
#rects1 = ax.bar(x , y_expected, width, yerr=0.0, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="royalblue", color="darkgrey",label='Single-photon fidelity from DSM')
rects1 = ax[0].bar(x , y_expected_re, width, yerr=0.0, ecolor="royalblue", alpha=0.5, color="royalblue", label='theory (expected)')
rects2 = ax[1].bar(x , y_expected_im, width, yerr=0.0, ecolor="royalblue", alpha=0.5, color="royalblue", label='theory (expected)')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_ylabel("Real Part",fontsize="15")
#ax.set_title('Scores by group and gender')
ax[0].set_xticks(x)
ax[0].set_xticklabels(labels)
ax[1].tick_params(axis='x', which='major', labelsize=20)
ax[1].set_ylabel("Imaginary Part",fontsize="15")


#fig.tight_layout()

#plt.text(0, 0, r'CQNET/FQNET Preliminary', fontsize=15, style='italic')
max_y = 1.25
plt.subplots_adjust(hspace = 0.05)
ax[0].set_ylim(-0.1, max_y)
ax[0].set_yticks((0, 0.25, 0.5, 0.75, 1))
ax[0].set_yticklabels((r'$\bf{0}$', r'$\bf{0.25}$',r'$\bf{0.5}$',r'$\bf{0.75}$', r'$\bf{1}$'))
ax[1].set_yticks((-0.05, 0, 0.05))
ax[1].set_yticklabels((r'$\bf{-0.05}$', r'$\bf{0}$',r'$\bf{0.05}$'))
#, (r'\bf{0}', r'\bf{0.25}',r'\bf{0.5}',r'\bf{0.75}', r'\bf{1}'), color='k', size=20)
ax[1].set_ylim(-0.08, 0.08)
fig.subplots_adjust(left=0.135, bottom=0.1, right=0.95, top=0.92)
ax[0].yaxis.set_label_coords(-0.12, 0.5)
ax[1].yaxis.set_label_coords(-0.12, 0.5)

##########################################
#horizontal red lines on top histogram bar
##########################################
for my_x, my_y in zip(x_expected,y_expected_re):
    line  = ax[0].hlines(y=my_y, xmin=my_x-width/2.0, xmax=my_x+width/2.0, colors='r', linestyles='dashed', label='',linewidth=2.5)
for my_x, my_y in zip(x_expected,y_expected_im):
    line2 = ax[1].hlines(y=my_y, xmin=my_x-width/2.0, xmax=my_x+width/2.0, colors='r', linestyles='dashed', label='',linewidth=2.5)


###########################
#add datapoints
#############################
err1 = ax[0].errorbar(x_mesured, y_measured_re, yerr=0.0, fmt='ok', ecolor="k",elinewidth=None, capsize=2, markerfacecolor='k', markersize=6,label='Data')
err2 = ax[1].errorbar(x_mesured, y_measured_im, yerr=0.0, fmt='ok', ecolor="k",elinewidth=None, capsize=2, markerfacecolor='k', markersize=6,label='Data')

##############################
#add cosmetics
##############################
ax[0].text(-0.4, 1.29, r'CQNET/FQNET 2020', fontsize=15, style='italic')
ax[0].text( 1.9, 1.29, r'Teleportation of $| e \rangle$', fontsize=15, style='italic')


####################################
#Legend
####################################
legend_elements = [
err1,
mpatch.Rectangle(xy=(3.0,1.2),width=0.07,height=0.03,edgecolor='royalblue',alpha=0.5,facecolor='red', lw=4,hatch='|',label='Theory (ideal)')
]

ax[0].legend(handles=legend_elements, loc='upper left')
ax[1].legend(handles=legend_elements, loc='upper left')
plt.savefig('density_matrix_plot_cqnet_with_spools.pdf')
