import numpy as np
import scipy.optimize

################################
#########DEFINE HOM FUNCTION####
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
    guess_t0 = 700
    guess_C = 220
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

###########################################
##########define sine function#############
###########################################
def sine_func(t, A, w, p, c):
    if A >= 0.0:
        return A * np.sin(w*t + p) + c
    else:
        return np.nan

###########################################
###############Define Sine fit#############
###########################################
def fit_sine(tt, yy,ee):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])
    print ('guess parameters:', guess)

    popt, pcov = scipy.optimize.curve_fit(sine_func, tt, yy, sigma = ee, absolute_sigma=True, p0=guess)
    perr = np.sqrt(np.diag(pcov))
    A, w, p, c = popt
    print(A, w, p,c)
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amplitude": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, 'fit_func': fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov), 'parameter_unc': perr}

###########################################
###############Define Sine fit#############
###########################################
def fit_sine_Sam(tt, yy,ee):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = 12881.089424177499#(np.max(yy)-np.min(yy))/2.0#np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])
    print ('guess parameters:', guess)

    popt, pcov = scipy.optimize.curve_fit(sine_func, tt, yy, sigma = ee, absolute_sigma=True, p0=guess)
    perr = np.sqrt(np.diag(pcov))
    A, w, p, c = popt
    print(A, w, p,c)
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amplitude": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, 'fit_func': fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov), 'parameter_unc': perr}
