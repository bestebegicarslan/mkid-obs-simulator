# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:54:28 2015

@author: cafolla
"""
import numpy as np
import matplotlib.pyplot as plt
from simulkid import simulatekid


def contourplot(spectra, skyvalues, filename):
    """ Takes as inputs:
    the spectra;
    the sky flux;
    and the name of the file where all the parameters are.
    Calculates a contour plot of SNR, magnitude vs exposure time """
    
    SNR = np.zeros((300,300))
    print('Now printing the spectra')
    print(spectra)
    for i in range(0,300,1):
        mag = 0.0 + i/10.0
        for j in range(0,300,1):
            exptime = 1.0 + 60.0*j
            SNR[i,j] = simulatekid(spectra*10.0**(-0.4*mag), exptime, skyvalues,filename,1, False )
    print('Printing the SNR')
    print(SNR)
    levels = np.array([3,10,20,100])
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.contour(np.arange(300.0), (np.arange(300.0)/10.0+0.0), SNR, levels, colors=['C0','C1','C2','C6'])
    ax.set_xlabel('Exposure Time (minutes)')
    ax.set_ylabel("V Magnitude (mag)")
    ax.set_xlim((1, 100))
    ax.set_ylim(35,0)
    ax.set_xscale('log')
    ax.set_title('Palomar MKID Camera SNR - Pulsar')
    #for i in levels(4):
    #    ax.plot(levels, i*levels, label='%ilevels' %i)

    #ax.legend()
    plt.show()
