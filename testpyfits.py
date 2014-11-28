import pyfits, pylab,sys, ds9
from pyraf import iraf

#es lo mismo que imheader

def displayHeader(fitsfile):
	hdulist = pyfits.open(fitsfile)
	print("List hdu length = %d" % len(hdulist))
	header = hdulist[0].header
	for k in header.keys():
		print "%s=%s" % (k, header[k])
	#print header


print("\n---------------------------------\nSTART %s " % sys.argv[1])
displayHeader(sys.argv[1])
