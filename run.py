
from __future__ import division
import os
import sys

# get the current directory
old = os.getcwd()

#go to the directory where all the modules to import are

folder = './modules to load'               # select the desired folder
os.chdir(folder)                            # access the folder
path = os.getcwd()
dirs = os.listdir(path)
sys.path.append(path)

# import all the modules
import reader
from select_parameters import select_parameters
from generatespectra import generatorspectra
from tablespectra import tablespectral
from skyflux import sky
from loadfilter import *
from contourplot import contourplot
import glob

# ask the user the parameter file to use
filename = select_parameters()

# import the parameters from the desired parameter file
filtername, spectraltype, mV,  startrange, endrange, arrsize, skyfile,\
                atmofile, telefile, pbfiltername, fudgefactor, expostime, diameter,\
                seeingvalue, quantumeff, startrange2, endrange2, vbessel, umag, gmag,\
                rmag,imag,zmag = reader(filename)    

# generate sky values and spectra
skyvalues = sky(filename)
if spectraltype < 0.0:
    library=(glob.glob('/home/software/mkid-obs-simulator/library_mkid/*'))
    print(library)
    template_sp = raw_input('Please select your template spectrum:')

    
    spectra = tablespectral(spectraltype, mV, filename, template_sp)
else:
    spectra = generatorspectra(spectraltype,mV, filename)

# print the graph!
print(contourplot(spectra,skyvalues, filename))
