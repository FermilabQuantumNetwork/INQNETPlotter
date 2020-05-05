import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def ThreeFoldProbability(na, mu, eta1, eta2, zeta):
    # Returns a three fold coincidence probability as a function of
    # Alice's mean photon number na,
    # Bob's/Charlie's mean photon number mu,
    # Bob's and Charlie's coupling efficiencies eta2 and eta1,
    # and Alice's and Charlie's photon indistinguishability zeta
    return 1 - 2/(1+eta1*mu*0.5)*np.exp(-(na*0.5*(1+(1-zeta**2)*0.5*eta1*mu))/(1+eta1*mu*0.5))+np.exp(-na)/(1+eta1*mu)+2/(1+0.5*eta1*mu*(1-eta2)+eta2*mu)*np.exp(-na*0.5*(1+(1-zeta**2)*0.5*eta1*mu*(1-eta2)+eta2*mu)/(1+0.5*eta1*mu*(1-eta2)+eta2*mu))-1/(1+eta2*mu)-1/(1+eta1*mu*(1-eta2)+eta2*mu)*np.exp(-na)

def HOM_visibility(na, mu, eta1, eta2, zeta):
    # Returns HOM visibility value for a three fold coincidence as a function of
    # Alice's mean photon number na,
    # Bob's/Charlie's mean photon number mu,
    # Bob's and Charlie's coupling efficiencies eta2 and eta1,
    # and Alice's and Charlie's photon indistinguishability zeta
   return (ThreeFoldProbability(na, mu, eta1, eta2, 0)-ThreeFoldProbability(na, mu, eta1, eta2, zeta))/ThreeFoldProbability(na, mu, eta1, eta2, 0)

def HOM_visibilityFix(na, zeta):
    return HOM_visibility(na, 0.008, 1.2e-2, 4.5e-3, zeta)

# Define vector of Alice's mean photon numbers
phn = np.linspace(0,0.019,100)

# Experimental values for Alice's mean photon number
#phn_exp = np.array([2.56e-03, 0.004325833333, 0.0070655, 0.001444444444, 0.0007251777778, 0.0003945111111, 2.02e-04, 2.93e-05])
phn_exp = np.array([0.01880336279, 0.01239950619, 0.00811547414, 0.005232164693, 0.002603087686, 0.001308850829, 0.0009395078605, 0.0004984076637, 0.0002576885445, 0.0001271122854, 0.000003974793952])

# Experimental HOM visibility values for three fold coincidence
#threefold_exp = np.array([0.6196319018, 0.568, 0.5897435897, 0.5398773006, 0.4594594595, 0.2840909091, 0.3333333333, -0.1052631579])
threefold_exp = np.array([0.4763840496, 0.5445480862, 0.6131045242, 0.6571668064, 0.6722054381, 0.6273458445, 0.6424050633, 0.4111675127, 0.1987179487, 0.2540983607, 0.03191489362])

# Error for experimental HOM visibilities
#threefold_err = np.array([0.04013199037, 0.03517453624, 0.02794265219, 0.06420039552, 0.08661422269, 0.1181502759, 0.1171213948, 0.2020452358])
threefold_err = np.array([0.01242701974, 0.01460191565, 0.01670432955, 0.01964410489, 0.02564113943, 0.03703216757, 0.03919559341, 0.06891310594, 0.09618808288, 0.1033167537, 0.1423687854])

# Fit the theory curve to experimental data.
# Free parameters are: Bob's/Charlie's mean photon number mu,
# Bob's and Charlie's coupling efficiencies eta2 and eta1,
# and photon indistinguishability zeta
popt, pcov = curve_fit(HOM_visibilityFix, phn_exp, threefold_exp, sigma=threefold_err, p0=[0.902], absolute_sigma=True)
# deviations of the fit parameters
perr = np.sqrt(np.diag(pcov))

print(popt)
print(perr)

# Calculate chi square value for the fit parameters
r = threefold_exp - HOM_visibilityFix(phn_exp, *popt)
chisq = np.sum((r/threefold_err)**2)
df = len(phn_exp)-1
print("chisq/df =",chisq/df)

# plot the fit curve with experimental data
#fig = plt.figure()

plt.rcParams.update({'lines.markeredgewidth': 1})
fig, ax = plt.subplots(1,1, num=304, sharex = True)
ax.errorbar(phn_exp, threefold_exp, yerr=threefold_err, label='experimental data', fmt='ob', ecolor="blue", elinewidth=None, capsize=2, markerfacecolor='blue', markersize=6)

#plt.plot(phn, HOM_visibility(phn, *popt), label='fit '+r'$\mu$=%0.3e $\pm$ %0.2e , $\zeta$=%5.3f $\pm$ %5.3f'' \n $\eta_1$=%0.2e$\pm$ %0.2e , $\eta_2$=%0.2e$\pm$ %0.2e' % (popt[0],perr[0],popt[3],perr[3],popt[1],perr[1],popt[2],perr[2]))
ax.plot(phn, HOM_visibilityFix(phn, *popt),'-r', label='fit '+r'$\zeta$=%5.4f $\pm$ %5.4f,'' \n $\mu$=%0.1e, $\eta_1$=%0.1e, $\eta_2$=%0.1e' % (popt, perr, 8e-3, 1.2e-2, 4.5e-3))
#plt.plot(phn,HOM_visibility(phn, popt[0], popt[1], popt[2], 0.9), '--g', label='same parameters but '+r'$\zeta$=0.9')
#plt.plot(phn,HOM_visibility(phn, popt[0], popt[1], popt[2], 0.95), '--r', label='same parameters but '+r'$\zeta$=0.95')
#plt.plot(phn, HOM_visibility(phn, 8e-3, 0.012, 0.0045, 0.91))

plt.xlabel('Alice\'s mean photon number '+r'$n_A$', fontsize="14")
plt.ylabel('HOM visibility', fontsize="14")

fig.subplots_adjust(left=0.12, bottom=0.12, right=0.95, top=0.92)

plt.legend(loc='lower right', fontsize="12", frameon=False)
plt.show()
