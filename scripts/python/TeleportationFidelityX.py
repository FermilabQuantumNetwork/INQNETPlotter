import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def ThreeFoldProbabilityX(ne,nl, mu, eta1, eta2, zeta, phi):
    # Returns the probability for a three fold coincidence between
    # detection event of one of the Charlie's detectors in the early
    # time-bin with a detection event of the other detector in the #
    # late time-bin with a detection on one of the interferometer outputs at Bob.
    # Parameters are:
    # Alice's mean-photon number in the early/late time-bin ne & nl,
    # Bob's/Charlie's mean photon number mu,
    # Bob's and Charlie's coupling efficiencies eta2 and eta1,
    # Alice's and Charlie's photon indistinguishability zeta,
    # interferometer phase shift phi.
    return 1 - 1/(1+eta1*mu*0.5)*np.exp(-ne*0.5*(1+0.5*(1-zeta**2)*eta1*mu)/(1+eta1*mu*0.5))-1/(1+eta1*mu*0.5)*np.exp(-nl*0.5*(1+0.5*(1-zeta**2)*eta1*mu)/(1+eta1*mu*0.5))+1/(1+eta1*mu*0.5)*np.exp(-ne*0.5*(1+0.5*(1-zeta**2)*eta1*mu)/(1+eta1*mu*0.5))*1/(1+eta1*mu*0.5)*np.exp(-nl*0.5*(1+0.5*(1-zeta**2)*eta1*mu)/(1+eta1*mu*0.5))-1/(1+eta2*mu)+1/(1+eta2*mu+eta1*0.5*mu*(1-eta2/2+eta2*mu/2))*np.exp(-ne*0.5*(1+eta2*mu+eta1*0.5*mu*(1-zeta**2)*(1-eta2/2+eta2*mu/2))/(1+eta2*mu+eta1*0.5*mu*(1-eta2/2+eta2*mu/2)))+1/(1+eta2*mu+eta1*0.5*mu*(1-eta2/2+eta2*mu/2))*np.exp(-nl*0.5*(1+eta2*mu+eta1*0.5*mu*(1-zeta**2)*(1-eta2/2+eta2*mu/2))/(1+eta2*mu+eta1*0.5*mu*(1-eta2/2+eta2*mu/2)))-1/((1+eta1*0.5*mu)*(1+eta2*mu+eta1*mu*0.5*(1-eta2)))*np.exp(-1/((1+eta1*0.5*mu)*(1+eta2*mu+eta1*mu*0.5*(1-eta2)))*((ne+nl)*0.5*(1+eta2*mu+(1-0.5*zeta**2)*eta1*mu*(1-0.5*eta2*(1-mu))+(1-zeta**2)*(1-eta2)*(mu*eta1/2)**2) - 0.25*np.sqrt(ne*nl)*zeta**2 *eta1*eta2*mu*(1+mu)*np.sin(phi)))


#def FidelityX(n, mu, eta1, eta2, zeta):
    # Returns fidelity estimate for a teleportation of a |+> state
    # as a function of Alice's mean photon number 2*n (we assume that the mean photon number in each time-bin is the same such that Alice's total mean photon number is 2*n)
    # Bob's and Charlie's coupling efficiencies eta2 and eta1,
    # and Alice's and Charlie's photon indistinguishability zeta
    # F = P3fold_max/(P3fold_max+P3fold_min)
    #return ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 1.5*np.pi)/(ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 1.5*np.pi)+ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 0.5*np.pi))

def FidelityX(n, zeta):
    mu = 0.008
    eta1 = 1.2e-2
    eta2 = 4.5e-3
    return ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 1.5*np.pi)/(ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 1.5*np.pi)+ThreeFoldProbabilityX(n, n , mu, eta1, eta2, zeta, 0.5*np.pi))
# Define vector of Alice's mean photon numbers
phn = np.linspace(0,0.018,300)

# Experimental values for Alice's mean photon number
#phn_exp = np.array([0.02693467038/2, 0.01683560384/2, 0.008483555984/2, 0.006664861755/2, 0.00439129691/2, 0.002984691927/2, 0.001900359071/2, 0.01180324379/2])
phn_exp = 0.5*np.array([0.02679911482, 0.01670004828, 0.01166768824, 0.008348000428, 0.006529306199, 0.004261887923, 0.002849136371, 0.001764803515, 0.0004356247063])

# Experimental values for the teleportation fidelity
#fidelity_exp = np.array([0.673, 0.74, 0.79, 0.82, 0.84, 0.85, 0.85, 0.78])
fidelity_exp = np.array([0.673, 0.736, 0.77, 0.802, 0.815, 0.831, 0.849, 0.855, 0.8165])

# Error for experimental fidelities
#fidelity_err = np.array([0.01, 0.01, 0.02, 0.03, 0.02, 0.04, 0.03, 0.02])
fidelity_err = np.array([0.006, 0.009, 0.013, 0.014, 0.018, 0.022, 0.024, 0.041, 0.02617250466])

popt, pcov = curve_fit(FidelityX, phn_exp, fidelity_exp, sigma=fidelity_err, p0=[0.90], absolute_sigma=True)
# deviations of the fit parameters
perr = np.sqrt(np.diag(pcov))

print(popt, perr)
# Calculate chi square value for the fit parameters
r = fidelity_exp - FidelityX(phn_exp, *popt)
chisq = np.sum((r/fidelity_err)**2)
df = len(phn_exp)-1
print("chisq/df =",chisq/df)

plt.rcParams.update({'lines.markeredgewidth': 1})
fig = plt.figure()

plt.errorbar(phn_exp, fidelity_exp, yerr=fidelity_err, label='experimental data', fmt='ob', ecolor="blue", elinewidth=None, capsize=2, markerfacecolor='blue', markersize=6)

#plt.plot(phn, FidelityX(phn, 0.01, 0.01, 0.01, 0.93))
plt.plot(phn, FidelityX(phn, *popt),'-r', label='fit '+r'$\zeta$=%5.4f $\pm$ %5.4f,'' \n $\mu$=%0.1e, $\eta_1$=%0.1e, $\eta_2$=%0.1e' % (popt, perr, 8e-3, 1.2e-2, 4.5e-3))
#plt.plot(phn, FidelityX(phn, popt[0], 1.2*popt[1], popt[2], popt[3]), label='fit with '+r'$\eta_{1}=1.2 \eta_{1fit}$')
#plt.plot(phn, FidelityX(phn, popt[0], 0.8*popt[1], popt[2], popt[3]), label='fit with '+r'$\eta_{1}=0.8 \eta_{1fit}$')

plt.xlabel('Alice\'s mean photon number '+r'$n_A$', fontsize="14"  )
plt.ylabel('Teleportation fidelity', fontsize="14")


plt.legend(loc='lower right', fontsize="12", frameon=False)
plt.show()
