import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f


##############################
#####define x-axis labels#####
##############################
#labels = [r'$| e \rangle$', r'$| \ell \rangle$', r'$| + \rangle$', 'average']

######################################
# bsm1 = early
# bsm2 = late
#####################################
bsm1 = [4, 5, 2, 5, 6, 9, 11, 6, 7, 6]#, 1, 1, 3]
bsm2 = [234, 214, 237, 206, 207, 195, 235, 190, 149, 148]#, 41, 10, 45]
totalbsm = [bsm1[i]+bsm2[i] for i in range(len(bsm1))]
bsm1_err = [b**0.5 for b in bsm1]
bsm2_err = [b**0.5 for b in bsm2]

print(len(bsm1))
print(len(bsm2))

fids = np.array([bsm2[i]/(total) for i, total in enumerate(totalbsm)])


def p_lo(alpha, n, N):
    quant_lo = f.ppf(alpha, 2*n, 2*(N-n+1), loc=0, scale=1)
    return n* quant_lo/(N-n+1 + n*quant_lo)
def p_up(alpha, n, N):
    quant_up = f.ppf(1-alpha, 2*(n+1), 2*(N-n), loc=0, scale=1)
    return (n+1)*quant_up/(N-n + (n+1)*quant_up)

fids_err_lo = np.array([fids[i]-p_lo(0.05,bsm2[i],total) for i,total in enumerate(totalbsm)])
fids_err_up = np.array([p_up(0.05,bsm2[i],total)-fids[i] for i,total in enumerate(totalbsm)])


#fids_err = np.array([fids[i]*((bsm2_err[i]/bsm2[i])**2 + ((bsm1_err[i]**2 + bsm2_err[i]**2)**0.5/(bsm1[i]+bsm2[i]))**2)**0.5 for i in range(len(bsm1))])


sum_bsm1, sum_bsm2 = 0, 0
cum_bsm1, cum_bsm2, cum_totalbsm = [], [], []
for i,b in enumerate(bsm1):
    sum_bsm1 = sum_bsm1 + b
    cum_bsm1.append(sum_bsm1)
    sum_bsm2 = sum_bsm2 + bsm2[i]
    cum_bsm2.append(sum_bsm2)
    cum_totalbsm.append(sum_bsm1+sum_bsm2)

cum_bsm1_err = [b**0.5 for b in cum_bsm1]
cum_bsm2_err = [b**0.5 for b in cum_bsm2]


cum_fids = np.array([cum_bsm2[i]/(cum_bsm1[i]+cum_bsm2[i]) for i in range(len(cum_bsm1))])

cum_fids_err_lo = np.array([cum_fids[i]-p_lo(0.05,cum_bsm2[i],total) for i,total in enumerate(cum_totalbsm)])
cum_fids_err_up = np.array([p_up(0.05,cum_bsm2[i],total)-cum_fids[i] for i,total in enumerate(cum_totalbsm)])
#cum_fids_err = np.array([cum_fids[i]*((cum_bsm2_err[i]/cum_bsm2[i])**2 + ((cum_bsm1_err[i]**2 + cum_bsm2_err[i]**2)**0.5/(cum_bsm1[i]+cum_bsm2[i]))**2)**0.5 for i in range(len(cum_bsm1))])


print("bsm1: ", bsm1)
print("bsm2: ", bsm2)
print("cumulative bsm1: ", cum_bsm1)
print("cumulative bsm2: ", cum_bsm2)
print("fids: ", fids)
print("fids_err_lo: ", fids_err_lo)
print("fids_err_up: ", fids_err_up)
print("cum_fids: ", cum_fids)
print("cum_fids_err_lo: ", cum_fids_err_lo)
print("cum_fids_err_up: ", cum_fids_err_up)






#x = np.arange(len(labels))  # the label locations
#print(x)
#x = [0, 9, 24, 33, 48, 57, 72, 81, 96, 105]#, 120, 129, 144]
#x = [0, 9, 24-1/6, 33-1/6, 48-1/6, 57-1/6, 72-1/6, 81-1/6, 96-1/6, 105-1/6, 120-1/6, 129-1/6, 144-1/6]
x = [9*i for i in range(10)]
x1 = np.array([n+9 for n in x])
#x0ticks=[0, 9, 18, 24, 33, 42, 48, 57, 66, 72, 81, 90, 96, 105, 114]#, 120, 129, 138, 144, 153]
x0ticks = [9*i for i in range(11)]
x1ticks = x1
width = 9  # the width of the bars

fig, axs = plt.subplots(2,1, num=304, sharex = True)

rects1 = axs[1].bar(x, fids, width, yerr=[fids_err_lo, fids_err_up], error_kw=dict(lw=2, capsize=4, capthick=2), align='edge', ecolor="darkgrey", color="royalblue",edgecolor="darkgrey",label='Fidelity per 9 Hour Period')


# Add some text for labels, title and custom x-axis tick labels, etc.
axs[1].set_ylabel("Fidelity",fontsize="14")
#ax.set_title('Scores by group and gender')
axs[1].set_xticks(x0ticks)
axs[1].tick_params(axis='x', which='major')
axs[1].set_xlabel("Hours Elapsed")

axs[0].set_ylim(0.96,1.005)
axs[0].errorbar(x1,cum_fids,yerr=[cum_fids_err_lo,cum_fids_err_up], color = "royalblue", fmt='-o', ecolor="darkgrey", capsize=4, label = "Cumulative Fidelity")
axs[0].set_xticks(x0ticks)
axs[0].set_ylabel("Fidelity", fontsize="14")
axs[1].set_xlabel("Elapsed Time (Hours)")



def autolabel(rects):
    for i, rect in enumerate(rects):
        height = rect.get_height()
        axs[1].annotate('{:.2f}'.format(height)+' $\pm$ ' + '$_{'+'{:.2f}'.format(fids_err_up[i])+'} ^{'+'{:.2f}'.format(fids_err_lo[i])+'}$',
                    xy = (rect.get_x()+rect.get_width()/1.8,0),
                    xytext = (0,3),
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=90, color = "white", style = "normal", fontsize=16)



autolabel(rects1)

#fig.tight_layout()

#plt.text(0, 0, r'CQNET/FQNET Preliminary', fontsize=15, style='italic')
axs[1].set_ylim(0, 1.3)
fig.subplots_adjust(left=0.12, bottom=0.1, right=0.95, top=0.92, hspace=0.1)
#horizontal lines
#axs[1].hlines(y=0.67, xmin=min(x0ticks)-0.4, xmax=max(x0ticks)+0.4, colors='k', linestyles='dashed', label='Classical Limit = 0.67')
#axs[1].hlines(y=0.96, xmin=min(x0ticks)-0.4, xmax=max(x0ticks)+0.4, colors='darkgrey', linestyles='dashed', label='Fidelity = 0.97')
axs[1].legend(loc="upper left")
axs[0].legend(loc="upper left")
plt.text(-0.6, 3.115, r'CQNET/FQNET Preliminary 2020', fontsize=15, style='italic')
plt.savefig('longterm_early_fidelity.pdf')
plt.show()
