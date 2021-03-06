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
from libs.function_definitions import fit_sine #get sine fit function
from libs.helper_utilities import csv_parser_keys_xyz# get x,y,z keys csv parser helper
from libs.helper_utilities import command_line_parser#get command_line_parser

start_time = time.time()
x = []#x-axis plot
y = []#bsm1 counts
z = []#bsm2 counts
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
#output_file_name = 'XTeleport2020Feb7_xteleport_visibility_no_spools_cqnet_paper_April20_1.pdf'
output_file_name = 'XTeleport2020Mar17_xteleport_visibility_with_spools_cqnet_paper_April20_1.pdf'
if parser.output_file_name == None:
    print('[WARNING] Did not provide an output_file_name. Will use default name:', output_file_name )
    print('[HELP] Run: python plot_hom_and_fit.py --help')
else:
    output_file_name = parser.output_file_name


##############################
###Parse csv file and get list
##############################
x,y,z = csv_parser_keys_xyz(input_file_name, 'Temp_(C)', 'bsm1_counts_per_40min', 'bsm2_counts_per_40min')##Spools
#x,y,z = csv_parser_keys_xyz(input_file_name, 'Temp_(C)', 'bsm1_counts_per_12min', 'bsm2_counts_per_12min')## no-Spools

print('max y from data:', np.max(y))
##########################################
##########PERFORM FIT for BSM1############
##########################################
y_unc = np.sqrt(y)#assign poisson uncertainty to datapoints
fine_x   = np.linspace(min(x), max(x), 5000)#guessing it get 100 equaly spaced points
ent_visibility_fit_result = fit_sine(x, y, y_unc)## calls sine function model and also peforms fit
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


##########################################
##########PERFORM FIT for BSM1############
##########################################
z_unc = np.sqrt(y)#assign poisson uncertainty to datapoints
#fine_x   = np.linspace(min(x), max(x), 5000)#guessing it get 100 equaly spaced points
ent_visibility_fit_result = fit_sine(x, z, z_unc)## calls sine function model and also peforms fit
sine_fit_eval_z   = ent_visibility_fit_result['fit_func'](fine_x)# get fit function from the return list and evaluate for differen x-values
amplitude_z       = ent_visibility_fit_result["amplitude"]#get amplitude parameter of the model
omega_z           = ent_visibility_fit_result["omega"]#get omega parameter from model
parameter_unc_z   = ent_visibility_fit_result['parameter_unc']#get parameter uncertainty
phase_z           = ent_visibility_fit_result['phase']#get phase inside sine
offset_z          = ent_visibility_fit_result['offset']#get y-axis offset
print("amplitude: ", amplitude_z)
print("omega: ", omega_z)
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

print('found_top-> ', min_t,' ', min_fit_function)
print('found_top-> ', max_t,' ', max_fit_function)
#bottom plot
min_fit_function_z = 99999999.
max_fit_function_z = 0.0
min_t_z  = -1.
max_t_z  = -1.

for i_t in fine_x:
    current_value_z = amplitude_z*np.sin(omega_z*i_t + phase_z)+offset_z
    #get max_t
    if  current_value_z > max_fit_function_z:
        max_fit_function_z = current_value_z
        max_t_z = i_t
    #get min_t
    if current_value_z < min_fit_function_z:
        min_fit_function_z = current_value_z
        min_t_z = i_t

print('found_bottom-> ', min_t_z,' ', min_fit_function_z)
print('found_bottom-> ', max_t_z,' ', max_fit_function_z)

######################################
##    get min,max counts from fit  ###
##compute visibility out of min,max###
######################################
max_count_fit = np.max(sine_fit_eval)##it agrees with max_fit_function
min_count_fit = np.min(sine_fit_eval)##it agrees with min_fit_function
visibility    = (max_count_fit-min_count_fit)/(max_count_fit+min_count_fit)
#bottom plot
max_count_fit_z = np.max(sine_fit_eval_z)##it agrees with max_fit_function
min_count_fit_z = np.min(sine_fit_eval_z)##it agrees with min_fit_function
visibility_z    = (max_count_fit_z-min_count_fit_z)/(max_count_fit_z+min_count_fit_z)


##################################
#####uncertainty propagation######
##################################
#get individual uncertainties
sigma_amplitude = parameter_unc[0]
sigma_omega     = parameter_unc[1]
sigma_phase     = parameter_unc[2]
sigma_offset    = parameter_unc[3]
#bottom plot
sigma_amplitude_z = parameter_unc_z[0]
sigma_omega_z     = parameter_unc_z[1]
sigma_phase_z     = parameter_unc_z[2]
sigma_offset_z    = parameter_unc_z[3]

########################################
#propagate uncertainty for max_count_fit
########################################
max_count_fit_unc  = np.power(np.sin(omega*max_t + phase)*sigma_amplitude,2)
max_count_fit_unc += np.power(amplitude*max_t*np.cos(omega*max_t + phase)*sigma_omega,2)
max_count_fit_unc += np.power(amplitude*np.cos(omega*max_t + phase)*sigma_phase,2)
max_count_fit_unc += np.power(sigma_offset,2)
max_count_fit_unc = np.sqrt(max_count_fit_unc)
#bottom plot
max_count_fit_unc_z  = np.power(np.sin(omega_z*max_t_z + phase_z)*sigma_amplitude_z,2)
max_count_fit_unc_z += np.power(amplitude_z*max_t_z*np.cos(omega_z*max_t_z + phase_z)*sigma_omega_z,2)
max_count_fit_unc_z += np.power(amplitude_z*np.cos(omega_z*max_t_z + phase_z)*sigma_phase_z,2)
max_count_fit_unc_z += np.power(sigma_offset_z,2)
max_count_fit_unc_z = np.sqrt(max_count_fit_unc_z)

########################################
#propagate uncertainty for min_count_fit
########################################
min_count_fit_unc  = np.power(np.sin(omega*min_t + phase)*sigma_amplitude,2)
min_count_fit_unc += np.power(amplitude*min_t*np.cos(omega*min_t + phase)*sigma_omega,2)
min_count_fit_unc += np.power(amplitude*np.cos(omega*min_t + phase)*sigma_phase,2)
min_count_fit_unc += np.power(sigma_offset,2)
min_count_fit_unc = np.sqrt(max_count_fit_unc)
#bottom
min_count_fit_unc_z  = np.power(np.sin(omega_z*min_t_z + phase_z)*sigma_amplitude_z,2)
min_count_fit_unc_z += np.power(amplitude_z*min_t_z*np.cos(omega_z*min_t_z + phase_z)*sigma_omega_z,2)
min_count_fit_unc_z += np.power(amplitude_z*np.cos(omega_z*min_t_z + phase_z)*sigma_phase_z,2)
min_count_fit_unc_z += np.power(sigma_offset_z,2)
min_count_fit_unc_z = np.sqrt(max_count_fit_unc_z)

################################################################################
#propagate full uncertainty
#(A-B)/(A+B) --> sigma^2 = sigma_A^2 * 4B^2/(A+B)^4 + sigma_B^2 * 4A^2/(A+B)^4
################################################################################
total_counts = max_count_fit+min_count_fit
full_visibility_unc  = np.power(max_count_fit_unc*2.*min_count_fit/(total_counts*total_counts),2)
full_visibility_unc += np.power(min_count_fit_unc*2.*max_count_fit/(total_counts*total_counts),2)
full_visibility_unc  = np.sqrt(full_visibility_unc)
print ('individual uncertainties: ', parameter_unc)
print ('max_count_fit_unc = ', max_count_fit_unc)
print ('min_count_fit_unc = ', min_count_fit_unc)
print ('full visibility unc%: ', full_visibility_unc*100.)
print('(min,max,visibility) = (%f,$f,%f)' , (min_count_fit,max_count_fit,visibility))
#bottom
total_counts_z = max_count_fit_z+min_count_fit_z
full_visibility_unc_z  = np.power(max_count_fit_unc_z*2.*min_count_fit_z/(total_counts_z*total_counts_z),2)
full_visibility_unc_z += np.power(min_count_fit_unc_z*2.*max_count_fit_z/(total_counts_z*total_counts_z),2)
full_visibility_unc_z  = np.sqrt(full_visibility_unc_z)
print ('individual uncertainties: ', parameter_unc_z)
print ('max_count_fit_unc = ', max_count_fit_unc_z)
print ('min_count_fit_unc = ', min_count_fit_unc_z)
print ('full visibility unc%: ', full_visibility_unc_z*100.)
print('(min,max,visibility) = (%f,$f,%f)' , (min_count_fit_z,max_count_fit_z,visibility_z))

################################
######PLOTTING ONLY#############
################################
plt.rcParams.update({'lines.markeredgewidth': 1})
fig, ax = plt.subplots(1, num=304, sharex = True, sharey=True)
################################
######TOP Plot##################
################################
ax.errorbar(x, y, y_unc, fmt='or', ecolor="red",elinewidth=None, capsize=2, markerfacecolor='red', markersize=5)
ax.plot(fine_x, sine_fit_eval,'-r', label = r"$V_{+,1}$"+": {:.1f}".format(visibility*100.)+r" $\pm$ "+"{:.1f}".format(full_visibility_unc*100.)+ "%")
#ax.plot(fine_x, sine_fit_eval,'-r')
#set x-y axis labels
ax.legend(loc="upper left",bbox_to_anchor=(0.06, 0.99),fontsize="13", frameon=False)
#ax.set_ylabel("Three-fold coincidences / (12 min)",fontsize="16")
ax.set_ylabel("Three-fold coincidences / (40 min)",fontsize="16")
plt.xlabel('Interferometer Temperature '+r'($\degree$C)',fontsize="16")
ax.tick_params(axis="x", labelsize=14)
ax.tick_params(axis="y", labelsize=14)



###Set ticks and and tick labels to red
#ax.tick_params(axis='y',color='r')
#plt.setp(ax.get_yticklabels(), color="red")


################################
###Bottom Plot##################
################################
ax2 = ax.twinx()
ax2.tick_params(axis="y", labelsize=16)
ax2.errorbar(x, z, z_unc, fmt='ob', ecolor="blue",elinewidth=None, capsize=2, markerfacecolor='blue', markersize=5)
ax2.plot(fine_x, sine_fit_eval_z,'--b', label = r"$V_{+,2}$"+": {:.1f}".format(visibility_z*100.)+r" $\pm$ "+"{:.1f}".format(full_visibility_unc_z*100.)+ "%")
#ax2.plot(fine_x, sine_fit_eval_z,'-b')
#ax2.set_ylabel("Three-fold coincidences / (12 min)",fontsize="14",rotation=270)
ax2.tick_params(axis="y", labelsize=14)
#set x-y axis labels
#ax2.set_ylabel("Three-fold coincidences / (40 min)",fontsize="14")

#fig.axes[1].annotate("", xy=(0, 0.5), xytext=(0, 0), arrowprops=dict(arrowstyle="<-"))

###Set ticks and and tick labels to red
#ax2.tick_params(axis='y',color='b')
#plt.setp(ax2.get_yticklabels(), color="blue")
#ax.legend(loc="upper left",fontsize="11", frameon=False)
#move boundaries of pad inside the plot -- move to right and up

#make plot legend
plt.legend(loc="upper right",bbox_to_anchor=(1.02, 0.99),fontsize="13", frameon=False)



axis_offset = 0.01#define left and right offset from min and max x-position
ax.set_ylim(0, 1.6*max_count_fit)
ax2.set_ylim(0, 1.6*max_count_fit_z)
plt.xlim(min(x)-axis_offset, max(x)+axis_offset)

#plt.axvline(x=max(x), c='b')
# ax.spines['right'].set_color('blue')
# ax2.spines['right'].set_color('blue')
# ax2.spines['right'].set_linewidth(2.5)
# ax.spines['left'].set_color('red')
# ax2.spines['left'].set_color('red')
# ax2.spines['left'].set_linewidth(2.5)


##change x and y axis label possitions 0.5 is center of each axis
ax.yaxis.set_label_coords(-0.11, 0.5)
ax.xaxis.set_label_coords(0.5, -0.1)
#fig.subplots_adjust(left=0.05, bottom=0.12, right=2, top=0.92)
fig.subplots_adjust(left=0.15, bottom=0.15, right=0.92, top=0.92)

#ax.text(min(x)-axis_offset, 1.625*max_count_fit, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
ax.text(min(x)+1.1*axis_offset, 1.45*max_count_fit, "b)", fontsize=18)#, style='italic')
# ax.text(24.18, 225, r'$\leftarrow$', fontsize=30, color = 'r')
# ax2.text(24.86, 110, r'$\rightarrow$', fontsize=30, color = 'b')
ax.text(24.0985, 19.95, r'$\leftarrow$', fontsize=30, color = 'r')
ax2.text(24.525, 18.85, r'$\rightarrow$', fontsize=30, color = 'b')


combined_visibility = (visibility_z+visibility)/2.0
combined_vis_uncertainty = np.sqrt(full_visibility_unc*full_visibility_unc/4.0 + full_visibility_unc_z*full_visibility_unc_z/4)
#ax.text(max(x)-55*axis_offset, 1.4*max_count_fit, "Visibility: {:.2f}".format(combined_visibility*100.)+r" $\pm$ "+"{:.2f}".format(combined_vis_uncertainty*100.)+ "%", fontsize=15)
#plt.annotate(s='', xy=(1,1), xytext=(0,0), arrowprops=dict(arrowstyle='<->'))

print("--- %s seconds ---" % (time.time() - start_time))
#plt.show()
print('[INFO] Saving plot as <', output_file_name,'>')
plt.savefig(output_file_name)

plt.show()
