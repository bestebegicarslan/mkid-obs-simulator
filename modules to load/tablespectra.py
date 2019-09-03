import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
#from scipy.interpolate import interp1d
from pylab import *
import matplotlib.mlab as mlab
from astropy.io import ascii
from astropy.table import Table
from astropy.io import fits
from astropy.time import Time
import glob
from fundconstants import *
from loadfilter import loadfilter
from reader import reader

def tablespectral(spectraltype, mV, filename, template_sp):

 ffiltername, spectraltype, mV,  startrange, endrange, arrsize, skyfile,\
                atmofile, telefile, pbfiltername, fudgefactor, expostime, diameter,\
                seeingvalue, quantumeff, startrange2, endrange2, vbessel, umag, gmag,\
                rmag,imag,zmag = reader(filename)

 vf,fluxfilt = loadfilter(filename)

 data=ascii.read(str(template_sp))
 wl= (data['col1']/1000)*1e-8
 flux= data['col2']

# arrsize=10000

 wavelength =np.linspace(1e-5,9.999e-5 , num=arrsize,endpoint=True)
 nstep = len(wavelength)
 # spectra in 1 Angstrom bins from 0 to 9999 Angstroms
 spectra = np.zeros(nstep)

 for i in range(nstep):
  if wavelength[i]<min(wl):
   spectra[i] = 0.0
  if wavelength[i]>max(wl):
   spectra[i] = 0.0
  else:
   spectra[i]=np.interp(wavelength[i],wl,flux)

 print(len(spectra))
 print(spectra)
 print(len(wavelength))
 print(wavelength)
 # wavelengths = np.linspace(nstep)
 plt.plot(wavelength*1e8,spectra, marker='o',linestyle='none')
 plt.plot(wl*1e8,flux)
 plt.xlabel("Wavelength")
 plt.ylabel("Flux")

 #print(np.max(spectra))
 #print(np.max(spectra[startrange:endrange])) 
 #spectra = spectra/np.max(spectra)
 #fluxspec = np.sum(spectra)/(endrange-startrange)
 sel_fl_range= np.where((wavelength>=startrange*1e-8)&(wavelength<=endrange*1e-8))
 print('This is the range you are selecting :')
 print(sel_fl_range)
 print(wavelength[sel_fl_range[0]])
 print(spectra[sel_fl_range[0]])
 spectra = spectra/np.max(spectra[sel_fl_range[0]])
 fluxspec = np.sum(spectra[sel_fl_range[0]])/(endrange-startrange)
 spectra = spectra/ fluxspec

 fluxV = np.sum(vf[sel_fl_range[0]] * spectra[sel_fl_range[0]]) / (endrange-startrange)

 spectra = spectra * (fluxV/fluxfilt) * 3.63E-9 * (10.0 ** (-mV/2.5)) 

 wavelengths = np.arange(arrsize)
 plt.figure()
 plt.plot(wavelengths*1e8, spectra)
 plt.xlabel("Wavelength (Angstrom)")
 plt.ylabel("Spectral radiance")
 plt.legend()
 plt.show()
 #ascii.write(spectra,'spectra_5000.dat', overwrite=True)

 return spectra
