
import getopt,sys
try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["fitsDir="])
except getopt.GetoptError as err:
				# print help information and exit:
				print("Error in parsing args")
				print(str(err)) # will print something like "option -a not recognized"
				sys.exit(2)
#print("OPTIONS")
#print(opts)
#print("OPTIONS END")
fitsDir = None
for o, a in opts:
				#print("o is now >%s<" % o)
				if o == "--fitsDir":
								fitsDir = a
				else:
								print("option %s not recognized " % o)


if(fitsDir is None):
	print("fitsDir required. set --fitsDir flag!")
	sys.exit(0)	

import glob

import os, pyfits
from common import degToRad
from math import cos

zdField = "ZD"
airmassField = "AIRMASS"
for fitsfile in glob.glob("%s/*.fits" % fitsDir):
	try:
		hdulist = pyfits.open(fitsfile)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		continue		
	header = hdulist[0].header
	airmass = 0
	zd = 0	
	if(zdField in header.keys()):
		zdStr = header[zdField]
		zdArray = zdStr.split(":")
		if(len(zdArray)==3):
			zd = degToRad(int(zdArray[0]), int(zdArray[1]), int(zdArray[2]))
	if(airmassField in header.keys()):
		airmass = float(header[airmassField])

	print("airmass(ZD) = %2.4f , in header = %2.4f\n" %(1.0/cos(zd), airmass))

