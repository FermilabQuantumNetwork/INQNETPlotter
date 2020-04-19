import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import scipy.optimize
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import os
import time
from libs.function_definitions import fit_hom #get hom fit function
from libs.helper_utilities import csv_parser,csv_parser_keys_xy# get x,y csv parser helper
from libs.helper_utilities import command_line_parser#get command_line_parser

start_time = time.time()
x = []
y = []

################################
###get command line arguments###
################################
parser = command_line_parser.parse_args()

#########################################
### check for valid input input_file_name
#########################################
input_file_name = None
if parser.input_file_name == None:
    print('[ERROR] Must provide an input_file_name. EXIT!')
    print('[HELP] Run: python plot_hom_and_fit.py --help')
    exit()
else:
    input_file_name = parser.input_file_name

#############################
###check for output_file_name
###if not present use default
#############################
output_file_name = 'HOM.pdf'
if parser.output_file_name == None:
    print('[WARNING] Did not provide an output_file_name. Will use default name:', output_file_name )
    print('[HELP] Run: python plot_hom_and_fit.py --help')
else:
    output_file_name = parser.output_file_name


# ###############################
# #######get input file##########
# ###############################
# top_directory=os.popen('git rev-parse --show-toplevel')
# top_directory = top_directory.read()
# input_file_name=top_directory.rstrip("\n")+'/data/CQNET_March2020/HOM.csv'


##############################
###Parse csv file and get list
##############################
#x,y = csv_parser(input_file_name)
#x,y = csv_parser_keys_xy(input_file_name,'delay_(ps)','threefold_(counts_per_2min)')#no-spools
x,y = csv_parser_keys_xy(input_file_name,'delay_(ps)','threefold_(counts_per_600s)')#with-spools

################################
##########PERFORM FIT###########
################################
y_err = np.sqrt(y)#assign poisson uncertainty to datapoints
fineDelay= np.linspace(min(x), max(x), 100)#guessing it get 100 equaly spaced points
resbsm=fit_hom(x, y, y_err)## call function to define HOM model and also peforms fit
homfitArr = resbsm["fitfunc"](fineDelay)# get fit function from the return list of fit_hom
visib = resbsm["V"]#get visibility parameter of the model
perr = resbsm["perr"]#parameter uncertainty
print("t0: ",resbsm["t0"])
print("T: ",resbsm["T"])
print("R: ",resbsm["R"])
print("C: ",resbsm["C"])
print(perr[2])
print(perr)

#get minimum time at which minimum in HOM occurs
hom_min_from_git = resbsm['t0']
print('min count occur at: ', hom_min_from_git)
################################
######PLOTTING ONLY#############
################################
#get_y_max
y_max_val = np.max(y)

################################
#subtract time offset from min
#align min with zero
################################
x         = x - hom_min_from_git
fineDelay = fineDelay - hom_min_from_git
#create plot
plt.rcParams.update({'lines.markeredgewidth': 1})
fig, ax = plt.subplots(1,1, num=304, sharex = True)
ax.errorbar(x, y, np.sqrt(y), fmt='ob', ecolor="blue",elinewidth=None, capsize=2, markerfacecolor='blue', markersize=6)
#ax.errorbar(x, y, np.sqrt(y), fmt='.k',capsize=2)
#ax.plot(time_tab2_el_mins, bsm,  linestyle = '--', marker = '.', markersize = 8)
ax.plot(fineDelay,homfitArr,'-r', label = "Visibility: {:.1f}".format(visib*100.)+r" $\pm$ "+"{:.1f}".format(perr[2]*100)+ "%")
ax.set_ylabel("Three-fold coincidences / (2 min)",fontsize="14")

#set x-y axis labels
plt.legend(loc="upper right",fontsize="12", frameon=False)
plt.xlabel('Alice-Bob time delay [ps]',fontsize="14")
##change x and y axis label possitions 0.5 is center of each axis
ax.yaxis.set_label_coords(-0.085, 0.5)
ax.xaxis.set_label_coords(0.5, -0.085)
#
fig.subplots_adjust(left=0.12, bottom=0.12, right=0.95, top=0.92)
plt.ylim(0.5*np.min(y), 1.3*y_max_val)
#plt.xlim(-30, 1630)
axis_offset = 50.0#define left and right offset from min and max x-position
plt.xlim(min(x)-axis_offset, max(x)+axis_offset)
ax.text(min(x)-axis_offset, 1.315*y_max_val, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')

print("--- %s seconds ---" % (time.time() - start_time))
#plt.show()
print('[INFO] Saving plot as <', output_file_name,'>')
plt.savefig(output_file_name)
