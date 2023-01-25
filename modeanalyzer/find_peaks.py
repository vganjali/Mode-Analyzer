import os as os
modpath = os.path.split(__file__)[0]
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.signal import find_peaks as scp_find_peaks
from time import perf_counter_ns

def gauss(x, a, mu, sigma):                         # Single Gaussian curve
    return a*np.exp(-(x-mu)**2/(2*sigma**2))

def find_peaks(Data, WG_Width, Valley_Offset, FindPeak_thresh=0.5, FindPeak_mindist=1.0, \
               CurveFit_a_bounds=(0,np.inf), CurveFit_mu_bounds=(-np.inf,np.inf), CurveFit_sigma_bounds=(0,np.inf)):
    xdata = np.linspace(0, WG_Width, max(1000, len(Data)))
    ydata = np.interp(xdata, np.linspace(0, WG_Width, len(Data)), Data)
    Data = ydata
    ydata_peaks = ydata[:]
    Residual = -1
    with plt.style.context((['default', modpath+'/fitplotstyle'])):
        fig1 = plt.figure('Curve Fitting', figsize=(5.5, 3.2))
        ax1 = plt.gca() 
        plt.ion()
        plt.show()
        ax1.cla()
        ax1.set_xlabel(r'X [$\mu$m]')
        ax1.set_ylabel('Intensity [a.u.]')
        ax1.grid(True, which='both', color='lightgray', linestyle=':')
        ax1.minorticks_on()
        plt.plot(xdata, ydata, color='black', linestyle='-', linewidth=2, label="Actual Data")
        plt.subplots_adjust(left=0.23, bottom=0.26, right=0.99, top=0.8, wspace=0, hspace=0)
        Idx, Idx_xdata, FWHM, FWHM_STD, Peak_to_Valley, Peak_to_Valley_STD, Delta_X, Delta_X_STD, ydata_fit = [], [], [0], [0], [0], [0], [0], [0], []
        Valleys = []
        t0 = perf_counter_ns()
        if (np.amin(Data) != np.amax(Data)):
            try:
                Idx,_ = scp_find_peaks(Data, height=FindPeak_thresh, \
                distance=FindPeak_mindist/WG_Width*len(Data))
                # print(Idx)
            except Exception as excpt:
                print(excpt)
                pass
        #print(perf_counter_ns()-t0)
        t0 = perf_counter_ns()
        if (len(Idx) > 0):
            p0 = np.zeros(3*len(Idx))
            bnds = (-np.inf*np.ones(3*len(Idx)), np.inf*np.ones(3*len(Idx)))
            make_func = 'def multi_gauss(x'
            for n in range(len(Idx)):
                p0[3*n:3*n+3] = ydata[Idx[n]], xdata[Idx[n]], (CurveFit_sigma_bounds[0]+CurveFit_sigma_bounds[1])/2
                bnds[0][3*n:3*n+3], bnds[1][3*n:3*n+3] = \
                [CurveFit_a_bounds[0]*ydata[Idx[n]], xdata[Idx[n]]+CurveFit_mu_bounds[0], CurveFit_sigma_bounds[0]], \
                [CurveFit_a_bounds[1]*ydata[Idx[n]], xdata[Idx[n]]+CurveFit_mu_bounds[1], CurveFit_sigma_bounds[1]]
                make_func += ', var'+str(3*n)+', var'+str(3*n+1)+', var'+str(3*n+2)
            make_func += '):\n    y = 0.0'
            for n in range(len(Idx)):
                make_func += '\n    y += var'+str(3*n)+ \
                '*np.exp(-(x-var'+str(3*n+1)+')**2/(2*var'+str(3*n+2)+'**2))'
            make_func += '\n    return y'
            # print(make_func)
            exec(make_func)
            #print(perf_counter_ns()-t0)
            t0 = perf_counter_ns()
            # Apply wight for peak fitting
    ##        popt, pcov = curve_fit(eval('multi_gauss'), xdata, ydata, p0=p0, \
    ##                               sigma=(0.9 - 0.8*np.ceil((ydata-FindPeak_thresh)/np.amax(ydata))), bounds=bnds, method='trf')
            # no weighting applied
            popt, pcov = curve_fit(eval('multi_gauss'), xdata, ydata, p0=p0, bounds=bnds, method='trf', ftol=0.5, xtol=0.5)
            Peak_to_Valley = np.mean(np.array([*popt[0::3]]))
            Peak_to_Valley_STD = np.std(Peak_to_Valley)
            Idx_xdata = popt[1::3]
            FWHM = 2.35482*popt[2::3]       # convert sigma value to FWHM
            FWHM_STD = np.std(FWHM)
            Delta_X = np.mean(np.ediff1d(Idx_xdata))
            Delta_X_STD = np.std(np.ediff1d(Idx_xdata))
    #        for n in range(len(Idx)):
    #            try:
    #                ydata_peaks[Idx[n-1]+int((len(Data)/WG_Width)*FWHM[n-1]/2): \
    #                Idx[n]-int((len(Data)/WG_Width)*FWHM[n]/2)] = 0
    #            except:
    #                ydata_peaks[:Idx[n]-int((len(Data)/WG_Width)*FWHM[n]/2)] = 0
    #            try:
    #                ydata_peaks[Idx[n]+int((len(Data)/WG_Width)*FWHM[n]/2): \
    #                Idx[n+1]-int((len(Data)/WG_Width)*FWHM[n+1]/2)] = 0
    #            except:
    #                ydata_peaks[Idx[n]+int((len(Data)/WG_Width)*FWHM[n]/2):] = 0
    #        plt.plot(xdata, ydata_peaks, 'g--')
    #        popt, pcov = curve_fit(eval('multi_gauss'), \
    #        xdata, ydata_peaks, p0=p0, bounds=bnds)
    #        Peak_to_Valley = np.array([*popt[0::3]])
    #        Idx_xdata = popt[1::3]
    #        FWHM = 2.35482*popt[2::3]
            #print(perf_counter_ns()-t0)
            t0 = perf_counter_ns()
            if (len(Idx) > 1):
                Valleys = np.zeros(len(Idx)-1)
                for n in range(len(Idx)):
                    plt.plot(xdata, gauss(xdata, *popt[3*n:3*n+3]), linestyle=':', color='orange')
                    try:
                        Valleys[n] = np.mean(ydata[int((Idx[n]+Idx[n+1])/2-Valley_Offset/WG_Width*len(Data)): \
                                        int((Idx[n]+Idx[n+1])/2+Valley_Offset/WG_Width*len(Data))])
                        plt.plot(xdata[int((Idx[n]+Idx[n+1])/2-Valley_Offset/WG_Width*len(Data)): \
                                        int((Idx[n]+Idx[n+1])/2+Valley_Offset/WG_Width*len(Data))], \
                                ydata[int((Idx[n]+Idx[n+1])/2-Valley_Offset/WG_Width*len(Data)): \
                                        int((Idx[n]+Idx[n+1])/2+Valley_Offset/WG_Width*len(Data))], linewidth=3, color='magenta', linestyle='-', marker='.', markersize=3)
                    except:
                        pass
                    plt.plot([Idx_xdata[n]-FWHM[n]/2, Idx_xdata[n]+FWHM[n]/2], \
                    [gauss(Idx_xdata[n], *popt[3*n:3*n+3])/2, gauss(Idx_xdata[n], *popt[3*n:3*n+3])/2], linestyle='-', color='limegreen')
            else:
                Valleys = [np.mean(ydata[:int(Valley_Offset/WG_Width*len(Data))]),np.mean(ydata[-int(Valley_Offset/WG_Width*len(Data)):])]
        # Peak_to_Valley = np.mean(ydata[Idx]) - np.mean(Valleys)       # normalized to the highest peak
            #print(perf_counter_ns()-t0)
            t0 = perf_counter_ns()
            Peak_to_Valley = (1 - np.mean(Valleys)/np.mean(ydata[Idx]))     # normalized to the avg of peaks
            Peak_to_Valley_STD = np.std(ydata[Idx]/np.mean(ydata[Idx]))
            plt.plot([xdata[0], xdata[-1]], [np.mean(ydata[Idx]), np.mean(ydata[Idx])], linestyle='--', color='deepskyblue', label="Average Peak")
            plt.plot([xdata[0], xdata[-1]], [np.mean(Valleys), np.mean(Valleys)], linestyle='--', color='magenta', label="Average Valley")
            ydata_fit = eval('multi_gauss(xdata, *popt)')
            plt.plot(xdata, ydata_fit, linestyle='-.', color='blue', label="Fitted Curve")
            plt.plot(xdata[Idx], ydata[Idx], marker='o', linestyle='none', markersize=6, \
                    markerfacecolor='red', markeredgewidth=1, markeredgecolor='red')
            ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                ncol=2, mode="expand", borderaxespad=0., facecolor='white')
        # Residual = np.sum((ydata-ydata_fit)**2)
            Delta_X = np.mean(np.ediff1d(Idx_xdata))
            Delta_X_STD = np.std(np.ediff1d(Idx_xdata))
            #print(perf_counter_ns()-t0)
            t0 = perf_counter_ns()
    return Idx, Idx_xdata, FWHM, FWHM_STD, Peak_to_Valley, Peak_to_Valley_STD, Delta_X, Delta_X_STD, ydata_fit