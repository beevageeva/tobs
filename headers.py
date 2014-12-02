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
field = None
for o, a in opts:
				#print("o is now >%s<" % o)
				if o == "--fitsDir":
								fitsDir = a
				else:
								print("option %s not recognized " % o)

import glob

if(fitsDir):
	import os, pyfits
	filePrefix = "list_%s_" % field
	fieldValues = {}  #hash value -> file
	for fitsfile in glob.glob("%s/*.fits" % fitsDir):
		try:
			hdulist = pyfits.open(fitsfile)
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			continue		
		header = hdulist[0].header
		print("\nfitsfile %s" % fitsfile)
		print(header)


		
		




