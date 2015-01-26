import os,sys
import pyfits,numpy
import re
from pyraf import iraf

iraf.noao.imred(Stdout=1)

from configLocal import FILTERS, OUTPUTDIR
iraf.minmax.unlearn()
iraf.minmax.setParam('verbose', 'no')
iraf.minmax.setParam('force', 'yes')
iraf.minmax.setParam('update', 'yes')
for ft in FILTERS:	
	print("start minmax object filter: %s" % ft)
	iraf.minmax.setParam('images', os.path.join(OUTPUTDIR, "object", ft) + "/*.fits")
	iraf.minmax()

