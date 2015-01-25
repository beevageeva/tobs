import numpy as np
import sys
from pyraf import iraf

# Initialize IRAF with ccdred
iraf.noao.digiphot.daophot(Stdout=1)


def daofind(filelist, psfimage):
	iraf.datapars.setParam("exposure", "EXPTIME")
	iraf.datapars.setParam("airmass", "AIRMASS")
	iraf.datapars.setParam("filter", "INSFILTE")
	iraf.datapars.setParam("ccdread", "RDNOISE")
	iraf.datapars.setParam("gain", "GAIN")
	iraf.daopars.setParam("fitrad", "5.853")
	iraf.daopars.setParam("psfrad", "18.56")
	

	with open(filelist) as file1:
		for line in file1:
			filename = line.strip()
			y,z = np.loadtxt(filename + "-daoedit", usecols=[3,4], unpack=True)
			sigma = np.mean(y) 
			fwhm = np.mean(z)
			iraf.datapars.setParam("fwhmpsf", "%s" % str(fwhm)  )
			iraf.datapars.setParam("sigma", "%s" % str(sigma)  )

			iraf.allstar.setParam("image","%s" % filename	)
			iraf.allstar.setParam("photfile","%s.mag" % filename	)
			iraf.allstar.setParam("psfimage",psfimage	)
			iraf.allstar.setParam("allstarfile","%s.als"%filename	)
			iraf.allstar.setParam("rejfile","%s.arj"%filename	)
			iraf.allstar.setParam("subimage","%s.sub" %filename	)


			iraf.allstar(mode="h")
			



daofind(sys.argv[1], sys.argv[2])	

