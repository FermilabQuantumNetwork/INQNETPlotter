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
from libs.helper_utilities import csv_parser# get x,y csv parser helper


start_time = time.time()
x = []
y = []

##############################
###Parse csv file and get list
##############################
x,y = csv_parser('HOM.csv')

################################
##########PERFORM FIT###########
################################
y_err = np.sqrt(y)#assign poisson uncertainty to datapoints
fineDelay= np.linspace(min(x), max(x), 100)#guessing it get 100 equaly spaced points
resbsm=fit_hom(x, y, y_err)## call function to define HOM model and also peforms fit
homfitArr = resbsm["fitfunc"](fineDelay)# get fit function from the return list of fit_hom
visib = resbsm["V"]#get visibility parameter of the model
perr = resbsm["perr"]#NOT SURE WHAT THIS IS
print("t0: ",resbsm["t0"])
print("T: ",resbsm["T"])
print("R: ",resbsm["R"])
print("C: ",resbsm["C"])
print(perr[2])
print(perr)

################################
######PLOTTING ONLY#############
################################
plt.rcParams.update({'lines.markeredgewidth': 1})
fig, ax = plt.subplots(1,1, num=304, sharex = True)
ax.errorbar(x, y, np.sqrt(y), fmt='ob', ecolor="blue",elinewidth=None, capsize=2, markerfacecolor='blue', markersize=6)
#ax.errorbar(x, y, np.sqrt(y), fmt='.k',capsize=2)
#ax.plot(time_tab2_el_mins, bsm,  linestyle = '--', marker = '.', markersize = 8)
ax.plot(fineDelay,homfitArr,'-r', label = "Visibility: {:.1f}".format(visib*100.)+r" $\pm$ "+"{:.1f}".format(perr[2]*100)+ "%")
ax.set_ylabel("Three-fold coincidences / (25 min)",fontsize="14")
plt.legend(loc="upper right",fontsize="12", frameon=False)
#plt.legend(loc="upper right",fontsize="12")
plt.xlabel('Alice-Bob time delay [ps]',fontsize="14")
plt.ylim(0, 100)
plt.xlim(-30, 1630)
ax.text(3, 102, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')

print("--- %s seconds ---" % (time.time() - start_time))
#plt.show()
print('[INFO] Saving plot as <hom.pdf>')
plt.savefig('hom.pdf')
