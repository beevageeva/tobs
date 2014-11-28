import getopt,sys
try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["field=", "fitsDir=", "outDir="])
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
				if o == "--field":
								field = a
				elif o == "--fitsDir":
								fitsDir = a
				elif o == "--outDir":
								outDir = a
				else:
								print("option %s not recognized " % o)

if(field is None):
	print("field required. set --field flag!")
	sys.exit(0)	

if(outDir is None):
	print("outDir required. set --outDir flag!")
	sys.exit(0)	

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
		if(field in header.keys()):
			fieldValue = header[field]
			if(not fieldValue in fieldValues.keys()):
				fieldValues[fieldValue] = open(os.path.join(outDir, filePrefix + fieldValue), 'w')
			fieldValues[fieldValue].write("%s\n" % fitsfile)
	for fieldValue in fieldValues.keys():
		fieldValues[fieldValue].close()


print("listing %s in %s" % (filePrefix, outDir))
for f in glob.glob("%s/%s*" % (outDir, filePrefix)):
	print("Content of file %s:" % f)
	with open (f, "r") as myfile:
		print(myfile.read())

		
		




