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
from libs.function_definitions import fit_sine, fit_sine_Sam #get sine fit function
from libs.helper_utilities import csv_parser_keys_xyz# get x,y,z keys csv parser helper
from libs.helper_utilities import command_line_parser#get command_line_parser

start_time = time.time()
x = []#x-axis plot
y = []#y-axis plot
y_unc = []#y-axis uncetainty plot
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
output_file_name = 'entanglement_visibility_fit_Sam.pdf'
if parser.output_file_name == None:
    print('[WARNING] Did not provide an output_file_name. Will use default name:', output_file_name )
    print('[HELP] Run: python plot_hom_and_fit.py --help')
else:
    output_file_name = parser.output_file_name


##############################
###Parse csv file and get list
##############################
x,y,y_unc = csv_parser_keys_xyz(input_file_name, 'Temp_(C)', 'coins_per_30min', 'coinserr_per_30min')

print("x: ",x)
print("y ",y )
print('max y from data:', np.max(y))
################################
##########PERFORM FIT###########
################################
#y_err = np.sqrt(y)#assign poisson uncertainty to datapoints
fine_x   = np.linspace(min(x)-0.01, max(x)+0.01, 5000)#guessing it get 100 equaly spaced points
ent_visibility_fit_result = fit_sine_Sam(x, y, y_unc)## calls sine function model and also peforms fit
sine_fit_eval   = ent_visibility_fit_result['fit_func'](fine_x)# get fit function from the return list and evaluate for differen x-values
amplitude       = ent_visibility_fit_result["amplitude"]#get amplitude parameter of the model
omega           = ent_visibility_fit_result["omega"]#get omega parameter from model
parameter_unc   = ent_visibility_fit_result['parameter_unc']#get parameter uncertainty
phase           = ent_visibility_fit_result['phase']#get phase inside sine
offset          = ent_visibility_fit_result['offset']#get y-axis offset
print("amplitude: ", amplitude)
print("omega: ", omega)
print("offset: ", ent_visibility_fit_result['offset'])
print("phase: ",  ent_visibility_fit_result['phase'])
#print(perr[2])
#print(perr)

#######################################
##get real min_t and max_t to
##propagate uncertainty correctly
#######################################
min_fit_function = 99999999.
max_fit_function = 0.0
min_t  = -1.
max_t  = -1.

for i_t in fine_x:
    current_value = amplitude*np.sin(omega*i_t + phase)+offset
    #get max_t
    if  current_value > max_fit_function:
        max_fit_function = current_value
        max_t = i_t
    #get min_t
    if current_value < min_fit_function:
        min_fit_function = current_value
        min_t = i_t

print('found-> ', min_t,' ', min_fit_function)
print('found-> ', max_t,' ', max_fit_function)

######################################
##    get min,max counts from fit  ###
##compute visibility out of min,max###
######################################
max_count_fit = np.max(sine_fit_eval)##it agrees with max_fit_function
min_count_fit = np.min(sine_fit_eval)##it agrees with min_fit_function
visibility    = (max_count_fit-min_count_fit)/(max_count_fit+min_count_fit)

##################################
#####uncertainty propagation######
##################################
#get individual uncertainties
sigma_amplitude = parameter_unc[0]
sigma_omega     = parameter_unc[1]
sigma_phase     = parameter_unc[2]
sigma_offset    = parameter_unc[3]

#propagate uncertainty for max_count_fit
# max_count_fit_unc  = np.power(np.sin(omega*max_t + phase)*sigma_amplitude,2)
# max_count_fit_unc += np.power(amplitude*max_t*np.cos(omega*max_t + phase)*sigma_omega,2)
# max_count_fit_unc += np.power(amplitude*np.cos(omega*max_t + phase)*sigma_phase,2)
# max_count_fit_unc += np.power(sigma_offset,2)
# max_count_fit_unc = np.sqrt(max_count_fit_unc)
max_count_fit_unc = np.sqrt(np.power(sigma_amplitude,2)+np.power(sigma_offset,2))

#propagate uncertainty for min_count_fit
# min_count_fit_unc  = np.power(np.sin(omega*min_t + phase)*sigma_amplitude,2)
# min_count_fit_unc += np.power(amplitude*min_t*np.cos(omega*min_t + phase)*sigma_omega,2)
# min_count_fit_unc += np.power(amplitude*np.cos(omega*min_t + phase)*sigma_phase,2)
# min_count_fit_unc += np.power(sigma_offset,2)
# min_count_fit_unc = np.sqrt(max_count_fit_unc)
min_count_fit_unc = np.sqrt(np.power(sigma_amplitude,2)+np.power(sigma_offset,2))

#propagate full uncertainty
#(A-B)/(A+B) --> sigma^2 = sigma_A^2 * 4B^2/(A+B)^4 + sigma_B^2 * 4A^2/(A+B)^4
#max_count_fit_unc = 3698.4582722854#hack systematic
total_counts = max_count_fit+min_count_fit
full_visibility_unc  = np.power(max_count_fit_unc*2.*min_count_fit/(total_counts*total_counts),2)
full_visibility_unc += np.power(min_count_fit_unc*2.*max_count_fit/(total_counts*total_counts),2)
full_visibility_unc  = np.sqrt(full_visibility_unc)

print ('individual uncertainties: ', parameter_unc)
print ('max_count_fit_unc = ', max_count_fit_unc)
print ('min_count_fit_unc = ', min_count_fit_unc)
print ('full visibility unc%: ', full_visibility_unc*100.)
print('(min,max,visibility) = (%f,$f,%f)' , (min_count_fit,max_count_fit,visibility))

Fid_ent = (3*visibility+1)/4
Fid_ent_err = 3*full_visibility_unc/4
print("")
print("Entanglement Fidelity: ", 100*Fid_ent, " +- ", 100*Fid_ent_err, "%")
################################
######PLOTTING ONLY#############
################################
plt.rcParams.update({'lines.markeredgewidth': 1})
fig, ax = plt.subplots(1,1, num=304, sharex = True)
ax.errorbar(x, y, np.sqrt(y), fmt='ob', ecolor="blue",elinewidth=None, capsize=2, markerfacecolor='blue', markersize=6)
#ax.errorbar(x, y, np.sqrt(y), fmt='.k',capsize=2)
#ax.plot(time_tab2_el_mins, bsm,  linestyle = '--', marker = '.', markersize = 8)
ax.plot(fine_x, sine_fit_eval,'-r', label = r"$V_{ent}$"+": {:.1f}".format(visibility*100.)+r" $\pm$ "+"{:.1f}%".format(full_visibility_unc*100.))#+ "%"+"\n"+r"$A =$"+"{:.2f}, ".format(amplitude)+r"$\omega =$"+"{:.2f}, ".format(omega)+r"$\phi =$"+"{:.2f}, ".format(phase)+r"$C =$"+"{:.2f}".format(offset))

#set x-y axis labels
ax.set_ylabel("Coincidences / (30 min)",fontsize="16")
plt.xlabel("Interferometer Temperature "+r"($\degree$C)",fontsize="16")
##change x and y axis label possitions 0.5 is center of each axis
ax.yaxis.set_label_coords(-0.15, 0.5)
ax.xaxis.set_label_coords(0.5, -0.09)
#move boundaries of pad inside the plot -- move to right and up
#fig.subplots_adjust(left=0.16, bottom=0.12, right=0.95, top=0.92)
#make plot legend
plt.legend(loc="upper left",fontsize="16", frameon=False)
plt.setp(ax.get_xticklabels(), fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14)



axis_offset = 0.01#define left and right offset from min and max x-position
plt.ylim(0, 1.2*max_count_fit)
plt.xlim(x[len(x)-3]-2*axis_offset, max(x)+axis_offset)
#change margins
fig.subplots_adjust(left=0.16, bottom=0.12, right=0.95, top=0.92)
ax.text(x[len(x)-2]+4*axis_offset, 1.215*max_count_fit, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
#ax.text(x[len(x)-2]-axis_offset, 1.215*max_count_fit, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')

print("--- %s seconds ---" % (time.time() - start_time))
#plt.show()
print('[INFO] Saving plot as <', output_file_name,'>')
plt.savefig(output_file_name)

plt.show()
