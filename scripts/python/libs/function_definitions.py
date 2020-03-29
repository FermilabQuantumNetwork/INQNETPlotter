import numpy as np
import scipy.optimize

################################
#########DEFINE SIN FUNCTION####
################################
def fit_hom(tt, yy,ee):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    guess_V = 0.50   # excluding the zero frequency "peak", which is related to offset
    T = np.sqrt(0.5)
    R = np.sqrt(0.5)
    guess_T = np.sqrt(0.5)
    guess_R = np.sqrt(0.5)
    guess_sigma = 140
    guess_t0 = 840
    guess_C = 60
    guess = np.array([guess_t0, guess_C, guess_V,guess_sigma])
    #guess = np.array([guess_t0, guess_C, guess_V,guess_sigma, guess_T, guess_R])
    #guess = np.array([guess_t0, guess_C, guess_V,guess_T,guess_R,guess_sigma])
    #def homfunc(t, C, V, sigma):  return C*(1-(2*V*R*T)/(R**2 + T**2)*np.exp(-((t-860)**2)/(2*sigma**2)))
    def homfunc(t, t0, C, V,sigma):  return C*(1-(2*V*R*T)/(R**2 + T**2)*np.exp(-((t-t0)**2)/(2*sigma**2)))
    #def homfunc(t, t0, C, V,sigma, T, R):  return C*(1-(2*V*R*T)/(R**2 + T**2)*np.exp(-((t-t0)**2)/(2*sigma**2)))
    popt, pcov = scipy.optimize.curve_fit(homfunc, tt, yy, sigma = ee, absolute_sigma=True, p0=guess, bounds=((-np.inf, -np.inf, -np.inf, -np.inf), (np.inf, np.inf, np.inf, np.inf)))
    #C, V, sigma = popt
    #t0, C, V, sigma = popt
    t0, C, V, sigma= popt
    perr = np.sqrt(np.diag(pcov))
    fitfunc = lambda t: C*(1-(2*V*R*T)/(R**2 + T**2)*np.exp(-((t-t0)**2)/(2*sigma**2)))
    return {"t0": t0,"C": C, "V": V, "T": T, "R": R, "sigma": sigma, "fitfunc": fitfunc, "perr": perr}
