import numpy as np
import sys
from pyraf import iraf

# Initialize IRAF with ccdred
iraf.noao.digiphot.daophot(Stdout=1)

def daofind(filelist):
	iraf.datapars.setParam("exposure", "EXPTIME")
	iraf.datapars.setParam("airmass", "AIRMASS")
	iraf.datapars.setParam("filter", "INSFILTE")
	iraf.datapars.setParam("ccdread", "RDNOISE")
	iraf.datapars.setParam("gain", "GAIN")
	
	iraf.centerpars.setParam("calgorithm", "centroid")
	iraf.photpars.setParam("apertures", "17.56")
	iraf.fitskypars.setParam("annulus", "20.56")
	iraf.fitskypars.setParam("dannulus", "5")
	
	

	with open(filelist) as file1:
		for line in file1:
			filename = line.strip()
			y,z = np.loadtxt(filename + "-daoedit", usecols=[3,4], unpack=True)
			sigma = np.mean(y) 
			fwhm = np.mean(z)
			iraf.datapars.setParam("fwhmpsf", "%s" % str(fwhm)  )
			iraf.datapars.setParam("sigma", "%s" % str(sigma)  )
			iraf.daofind(filename, filename + "-daofind")
			
			iraf.phot(filename, coords=(filename + "-daofind"), output=(filename+".mag"))



daofind(sys.argv[1])	

