import sys,pyfits


fitsfile = sys.argv[1]


try:
	hdulist = pyfits.open(fitsfile)
except IOError as e:
	print "I/O error({0}): {1}".format(e.errno, e.strerror)
	sys.exit(0)
header = hdulist[0].header
print("\nfitsfile %s" % fitsfile)
print(header)
for k in header.keys():
	if(k.strip()!=""):	
		print("header[%s] = %s" % (k, header[k]))


		
		




