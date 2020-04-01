import matplotlib
import matplotlib.pyplot as plt
import numpy as np


##############################
#####define x-axis labels#####
##############################
labels = [r'$| e \rangle$', r'$| \ell \rangle$', r'$| + \rangle$', 'average']

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
    dsm_means = [0.9853, 0.9834, 0.8400, 0.8900]#Decoy State Method (DSM) teleportation results
    dsm_unc   = [0.0105, 0.0175, 0.0450, 0.0187]#DSM uncetainty
    qst_means = [0.9620, 0.9860, 0.8733, 0.9010]#Quamtum State Tomography (QST) teleportation results
    qst_unc   = [0.0186, 0.0064, 0.0417, 0.0288]#QST uncetainty
else:
    print('[INFO]: plotting no-spool data')
    ##########################################
    #####No-spools result from CQNET-March2020
    ##########################################
    dsm_means = [0.981, 0.9983, 0.9236, 0.944]#Decoy State Method (DSM) teleportation results
    dsm_unc   = [0.0321, 0.0246, 0.0794, 0.0332]#DSM uncetainty
    qst_means = [0.952, 0.959, 0.8566, 0.890]#Quamtum State Tomography (QST) teleportation results
    qst_unc   = [0.012, 0.013, 0.0153, 0.0132]#QST uncetainty


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
ax.tick_params(axis='x', which='major', labelsize=20)
ax.legend()

def autolabel1(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    ctr = 0
    for rect in rects:
        height = rect.get_height()
        #print ('height:', height)
        ax.annotate('{:.2f}'.format(height)+' $\pm$ ' + '{:.2f}'.format(dsm_unc[ctr]),
                    xy=(rect.get_x() + rect.get_width() / 2, 1.0),
                    xytext=(0, -180),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90,color='w',fontsize=14, style='normal')
        ctr = ctr + 1

def autolabel2(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    ctr = 0
    for rect in rects:
        height = rect.get_height()
        #print ('height:', height)
        ax.annotate('{:.2f}'.format(height)+' $\pm$ ' + '{:.2f}'.format(qst_unc[ctr]),
                    xy=(rect.get_x() + rect.get_width() / 2, 1.0),
                    xytext=(0, -180),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90,color='w',fontsize=14, style='normal')
        ctr = ctr + 1

autolabel1(rects1)
autolabel2(rects2)

#fig.tight_layout()

#plt.text(0, 0, r'CQNET/FQNET Preliminary', fontsize=15, style='italic')
max_y = 1.3
plt.ylim(0, max_y)
fig.subplots_adjust(left=0.12, bottom=0.1, right=0.95, top=0.92)
#horizontal lines
plt.hlines(y=0.66, xmin=-0.4, xmax=3.8, colors='k', linestyles='dashed', label='',)
plt.text(-0.6, 1.315, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
plt.savefig('var_plot.pdf')
#plt.show()
