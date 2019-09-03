import numpy as np
from fundconstants import *
from loadfilter import loadfilter
from reader import reader
from astropy.io import ascii
import matplotlib.pyplot as plt

def generatorspectra(spectype, mV, filename): 
    """Takes as inputs: 
    the spectral type and magnitude of an object;
    and the name of the file, where all the parameters are.
    Generates a spectra."""
    
    # import the parameters from the parameter file 
    ffiltername, spectraltype, mV,  startrange, endrange, arrsize, skyfile,\
                atmofile, telefile, pbfiltername, fudgefactor, expostime, diameter,\
                seeingvalue, quantumeff, startrange2, endrange2, vbessel, umag, gmag,\
                rmag,imag,zmag = reader(filename)    
    
    # take into account the filter    
    vf, fluxfilt = loadfilter(filename)

     # spectra in 1 Angstrom bins from 0 to 9999 Angstroms
    spectra = np.zeros(arrsize)

    # Generate a blackbody spectra if spectype > 100
    if spectype > 100: # if spectral type < 100, then power law with slope type
        T = spectype    # blackbody temperature is given by the spectral type
        
        # wavelength in cm; array starts from 1 to avoid division by zero
        wavelength = np.arange(1,arrsize) * 1E-8  
        spectra[1:,] = (np.pi*2.0*h*c**2/wavelength**5)\
        /( np.exp(np.longfloat(h*c/(wavelength*k*T)))-1.0 ) #Planck's law

       # ascii.write(spectra,'generatespectra_5000.dat', overwrite=True)
        
        wavelengthss = np.arange(arrsize) *1E-8              #chech the spectra
        plt.plot(wavelengthss*1e8,spectra, marker='o',linestyle='none')
        plt.xlabel("Wavelength")
        plt.ylabel("Spectra")


    # Generate a power law spectra if spectype is smaller or equal to 100
    if spectype <= 100:        
        powerbase = np.arange(1,arrsize)*1e-8
        # start from 1 to avoid problems when dividing by zero
        spectra[1:,] = powerbase ** spectype

        wavelengthss = np.arange(arrsize)            #chech the spectra
        plt.plot(wavelengthss,spectra, marker='o',linestyle='none')
        plt.xlabel("Wavelength")
        plt.ylabel("Spectra")

    
    # normalize
    print('this is the spectra you are selecting :')
    print(spectra[startrange:endrange])
    spectra = spectra/np.max(spectra[startrange:endrange])  
    fluxspec = np.sum(spectra[startrange:endrange])/(endrange-startrange)
    spectra = spectra/ fluxspec
    
    # normalised convolution of spectra and filter
    fluxV = np.sum(vf[startrange:endrange] * spectra[startrange:endrange]) / (endrange-startrange) 
    
    # Normalize to specified mV - result should be in erg/s/cm^2/Angstrom
    spectra = spectra * (fluxV/fluxfilt) * 3.63E-9 * (10.0 ** (-mV/2.5)) # fluxfilt is flux from the filter (default is V filter)
    
       # debug below: check the spectra by plotting it
    wavelengths = np.arange(arrsize) *1E-8    
    plt.figure()
    plt.plot(wavelengths*1E8, spectra)
    plt.xlabel("Wavelength (Angstrom)")
    plt.ylabel("Spectral radiance")
    plt.legend()
    plt.show()
       
#    print "mAB at 6000 Angstroms = ",-2.5*np.log10(spectra[6000]) - 21.1 
    return spectra   
