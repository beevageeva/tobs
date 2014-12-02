from pyraf import iraf
from glob import glob
import numpy as np

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.ccdred(Stdout=1)

IMGDIR = "imagenesfits" 

BIAS_SEC= "[1025:1056,1:1024]"
DATA_SEC= "[1:1024,1:1024]"

def trimImages():
	print "TrimAndOverscan start"
	iraf.ccdproc.setParam('zerocor', 'no')
	iraf.ccdproc.setParam('flatcor', 'no')
	iraf.ccdproc.setParam('fixpix', 'no')
	iraf.ccdproc.setParam('darkcor', 'no')
	iraf.ccdproc.setParam('illumcor', 'no')
	iraf.ccdproc.setParam('trim', 'yes')
	iraf.ccdproc.setParam('trimsec', DATA_SEC)
	iraf.ccdproc.setParam('overscan', 'yes')
	iraf.ccdproc.setParam('biassec', BIAS_SEC)
	iraf.ccdproc.setParam("images", "imagenesfits/*.fits")
	#online
	iraf.ccdproc.setParam('output', '')
	iraf.ccdproc()
	print "TrimAndOverscan end"
	

trimImages()
