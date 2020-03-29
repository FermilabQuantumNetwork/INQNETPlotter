import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# labels = [r'$| e \rangle$', r'$| \ell \rangle$', r'$| + \rangle$', r'', 'average']
# men_means = [0.9792, 0.9925, 0.9028, -1.0, 0.944325]
# dsm_unc = [0.0127, 0.0058, 0.0589, -1.0, 0.0297]
# women_means = [0.959, 0.952, 0.8566, -10.0, 0.90605]
# qst_unc = [0.028, 0.0354, 0.0162, -10.0, 0.0139]

labels = [r'$| e \rangle$', r'$| \ell \rangle$', r'$| + \rangle$', 'average']
men_means = [0.9792, 0.9925, 0.9028, 0.944325]
dsm_unc = [0.0127, 0.0058, 0.0589, 0.0297]
women_means = [0.959, 0.952, 0.8566, 0.90605]
qst_unc = [0.028, 0.0354, 0.0162, 0.0139]

#x = np.arange(len(labels))  # the label locations
#print(x)
x = np.array([0.0,1.0,2.0,3.4])
print (x)
width = 0.45  # the width of the bars

fig, ax = plt.subplots(1,1, num=304, sharex = True)
#rects1 = ax.bar(x - width/2, men_means, width, yerr=dsm_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="royalblue", color="darkgrey",label='Single-photon fidelity from DSM')
#rects2 = ax.bar(x + width/2, women_means, width, yerr=qst_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="darkgrey", color="royalblue", label='Fidelity from QST')

#rects1 = ax.bar(x - width/2, men_means, width, yerr=dsm_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="royalblue", color="darkgrey",label='Single-photon fidelity from DSM')
rects2 = ax.bar(x , women_means, width, yerr=qst_unc, error_kw=dict(lw=2, capsize=4, capthick=2), ecolor="darkgrey", color="royalblue", label='Fidelity from QST')



# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("Fidelity",fontsize="14")
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

def autolabel1(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    ctr = 0
    for rect in rects:
        height = rect.get_height()
        print ('height:', height)
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
        print ('height:', height)
        ax.annotate('{:.2f}'.format(height)+' $\pm$ ' + '{:.2f}'.format(qst_unc[ctr]),
                    xy=(rect.get_x() + rect.get_width() / 2, 1.0),
                    xytext=(0, -180),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90,color='w',fontsize=14, style='normal')
        ctr = ctr + 1

#autolabel1(rects1)
autolabel2(rects2)

#fig.tight_layout()

#plt.text(0, 0, r'CQNET/FQNET Preliminary', fontsize=15, style='italic')
plt.ylim(0, 1.2)
#horizontal lines
plt.hlines(y=0.66, xmin=-0.4, xmax=3.8, colors='k', linestyles='dashed', label='',)
plt.text(-0.5, 1.22, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
plt.savefig('var_plot.pdf')
#plt.show()
