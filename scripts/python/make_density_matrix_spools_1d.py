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
from libs.helper_utilities import command_line_parser#get command_line_parser

#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import os
import time



###############################
###get command line arguments###
################################
parser = command_line_parser.parse_args()

#########################################
### check for valid input _teleportation_type
#########################################
_teleportation_type = None
if parser.teleportation_type == None:
    print('[ERROR] Must provide an teleportation_type. EXIT!')
    print('[HELP] Run: python make_density_matrix_spools_1d.py --help')
    exit()
else:
    _teleportation_type = parser.teleportation_type

############################
###spool vs no-spool option
############################
_spools = None
if parser.spools == None:
    print('[ERROR] Must provide spool=True or spool=False. EXIT!')
    print('[HELP] Run: python make_density_matrix_spools_1d.py --help')
    exit()
else:
    _spools = parser.spools

#############################
###check for output_file_name
###if not present use default
#############################
output_file_name = 'HOM.pdf'
if parser.output_file_name == None:
    print('[WARNING] Did not provide an output_file_name. Will use default name:', output_file_name )
    print('[HELP] Run: python make_density_matrix_spools_1d.py --help')
else:
    output_file_name = parser.output_file_name


##############################
#####define x-axis labels#####
##############################
labels = [r'$| e \rangle \langle e |$', r'$| e \rangle \langle  \ell |$', r'$| \ell  \rangle \langle e |$', r'$| \ell  \rangle \langle \ell |$']

#--------------------------------------
# the label locations -- equally spaced
#--------------------------------------
data_shift = 0.0
x = np.array([0.0,1.0,2.0,3])
x_mesured  = []
x_expected = []
y_measured_re = []
y_measured_im = []
y_expected_re = []
y_expected_im = []

for i in x:
    x_mesured.append(i-data_shift);
    x_expected.append(i+data_shift);

if  _spools == False:
    if _teleportation_type == 'early':
        y_measured_re = np.array([0.041, -0.026 , -0.026, 0.959])
        y_measured_im = np.array([0.0, 0.009 , -0.009, 0.0])
    elif _teleportation_type == 'late':
        y_measured_re = np.array([0.952,-0.037,-0.037,0.048])
        y_measured_im = np.array([0.0,-0.059,0.059,0.0])
    elif _teleportation_type == 'plus':
        y_measured_re = np.array([0.517,0.350,0.350,0.483])
        y_measured_im = np.array([0.0,-0.002,0.002,0.0])
    else:
        print('[ERROR] not valid teleportation type')
        exit()
else:
    if _teleportation_type == 'early':
        y_measured_re = np.array([0.014, 0.035 , 0.035, 0.986])
        y_measured_im = np.array([0.0, 0.009 , -0.009, 0.0])
    elif _teleportation_type == 'late':
        y_measured_re = np.array([0.962,-0.056,-0.056,0.038])
        y_measured_im = np.array([0.0,-0.042,0.042,0.0])
    elif _teleportation_type == 'plus':
        y_measured_re = np.array([0.515,0.331,0.331,0.485])
        y_measured_im = np.array([0.0,0.029,-0.029,0.0])
    else:
        print('[ERROR] not valid teleportation type')
        exit()

######################
##Setting Ideal Values
######################
if _teleportation_type == 'early':
    y_expected_re = np.array([0.0, 0.0 , 0.0, 1.0])
    y_expected_im = np.array([0.0, 0.0, 0.0, 0.0])
elif _teleportation_type == 'late':
    y_expected_re = np.array([1.0, 0.0, 0.0, 0.0])
    y_expected_im = np.array([0.0, 0.0, 0.0, 0.0])
elif _teleportation_type == 'plus':
    y_expected_re = np.array([0.5, 0.5, 0.5, 0.5])
    y_expected_im = np.array([0.0, 0.0, 0.0, 0.0])
else:
    print('[ERROR] not valid teleportation type')
    exit()


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
ax[1].set_yticks((-0.15,-0.1,-0.05, 0, 0.05, 0.1,0.15))
ax[1].set_yticklabels((r'$\bf{-0.15}$',r'$\bf{-0.1}$',r'$\bf{-0.05}$', r'$\bf{0}$',r'$\bf{0.05}$',r'$\bf{1.0}$',r'$\bf{0.15}$'))
#, (r'\bf{0}', r'\bf{0.25}',r'\bf{0.5}',r'\bf{0.75}', r'\bf{1}'), color='k', size=20)
ax[1].set_ylim(-0.2, 0.2)
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
#ax[0].text( 1.9, 1.29, r'Teleportation of $| e \rangle$', fontsize=15, style='italic')


####################################
#Legend
####################################
legend_elements = [
err1,
mpatch.Rectangle(xy=(3.0,1.2),width=0.07,height=0.03,edgecolor='royalblue',alpha=0.5,facecolor='red', lw=4,hatch='|',label='Theory (ideal)')
]

if _teleportation_type == 'early':
    ax[0].legend(handles=legend_elements, loc='upper center')
    ax[1].legend(handles=legend_elements, loc='upper center')
    ax[0].text( 1.85, 1.29, r'Teleportation of $| e \rangle$', fontsize=15, style='italic')
elif _teleportation_type == 'late':
    ax[0].legend(handles=legend_elements, loc='upper center')
    ax[1].legend(handles=legend_elements, loc='upper center')
    ax[0].text( 1.85, 1.29, r'Teleportation of $| \ell \rangle$', fontsize=15, style='italic')
elif _teleportation_type == 'plus':
    ax[0].legend(handles=legend_elements, loc='upper center')
    ax[1].legend(handles=legend_elements, loc='upper center')
    ax[0].text( 1.85, 1.29, r'Teleportation of $|+\rangle$', fontsize=15, style='italic')

plt.savefig('density_matrix_plot_cqnet_with_spools.pdf')
