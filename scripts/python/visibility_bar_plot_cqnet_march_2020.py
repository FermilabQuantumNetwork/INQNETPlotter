import matplotlib
import matplotlib.pyplot as plt
import numpy as np


##############################
#####define x-axis labels#####
##############################
labels = [r'$| e \rangle$', r'$| l \rangle$', r'$|+\rangle$', 'Average']

######################################
#flag to determin what data to plot
#is_spools_ = True -> plot spool data
#####################################
is_spools_ = False
#define lists for plot
dsm_means = []
dsm_unc = []
qst_means = []
qst_unc = []

if is_spools_ :
    ##########################################
    #####Spools result from CQNET-March2020
    ##########################################
    filename='summary_teleportation_plot_cqnet_with_spools.pdf'
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
    filename='summary_teleportation_plot_cqnet_no_spools.pdf'
    dsm_means = [0.9925, 0.9792, 0.9028, 0.9304833333]#Decoy State Method (DSM) teleportation results
    dsm_unc   = [0.0058, 0.0127, 0.0589, 0.03933555432]#DSM uncertainty
    qst_means = [0.952, 0.959, 0.85, 0.8851666667]#Quamtum State Tomography (QST) teleportation results
    qst_unc   = [0.012, 0.013, 0.016, 0.01106671687]#QST uncertainty


#x = np.arange(len(labels))  # the label locations
#print(x)
x = np.array([0.0,1.0,2.0,3.4])
width = 0.35  # the width of the bars

fig, ax = plt.subplots(1,1, num=304, sharex = True)
rects1 = ax.bar(x - width/2, dsm_means, width, yerr=dsm_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="royalblue", color="darkgrey",label='Single-photon fidelity from DSM')
rects2 = ax.bar(x + width/2, qst_means, width, yerr=qst_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="darkgrey", color="royalblue", label='Fidelity from QST')
#rects1 = ax.bar(x - width/2.5, men_means, width, yerr=dsm_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="royalblue", color="darkgrey",label='Single-photon fidelity from DSM')
#rects2 = ax.bar(x + width/2.5, qst_means, width, yerr=qst_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="darkgrey", color="royalblue", label='Fidelity from QST')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("Fidelity",fontsize="20")
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.tick_params(axis='x', which='major', labelsize=16)
ax.tick_params(axis='y', which='major', labelsize=16)
ax.legend(fontsize=14)

def autolabel1(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    ctr = 0
    for rect in rects:
        height = rect.get_height()
        #print ('height:', height)
        ax.annotate('{:.1f}'.format(100*height)+'$\pm$' + '{:.1f}'.format(100*dsm_unc[ctr])+"%",
                    xy=(rect.get_x() + rect.get_width() / 2, 1.0),
                    xytext=(0, -180),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90,color='w',fontsize=16, style='normal')
        ctr = ctr + 1

def autolabel2(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    ctr = 0
    for rect in rects:
        height = rect.get_height()
        #print ('height:', height)
        ax.annotate('{:.1f}'.format(100*height)+'$\pm$' + '{:.1f}'.format(100*qst_unc[ctr])+"%",
                    xy=(rect.get_x() + rect.get_width() / 2, 1.0),
                    xytext=(0, -180),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90,color='w',fontsize=16, style='normal')
        ctr = ctr + 1

autolabel1(rects1)
autolabel2(rects2)

#fig.tight_layout()

#plt.text(0, 0, r'CQNET/FQNET Preliminary', fontsize=15, style='italic')
max_y = 1.3
plt.ylim(0, max_y)
fig.subplots_adjust(left=0.13, bottom=0.1, right=0.95, top=0.92)
#fig.subplots_adjust(left=0.13, bottom=0.1, right=0.95, top=0.98)
#horizontal lines
plt.hlines(y=0.66, xmin=-0.4, xmax=3.8, colors='k', linestyles='dashed', label='',)
plt.text(-0.5, 1.2, "a)", fontsize=20)#, style='italic')
plt.text(-0.6, 1.315, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
plt.savefig(filename)
plt.show()
