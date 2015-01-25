import os, shutil, re
import pyfits
from glob import glob


from configLocal import  OUTPUTDIR, FILTERS

import getopt,sys
try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["objectName="])
except getopt.GetoptError as err:
				# print help information and exit:
				print("Error in parsing args")
				print(str(err)) # will print something like "option -a not recognized"
				sys.exit(2)
#print("OPTIONS")
#print(opts)
#print("OPTIONS END")
objectName = None
for o, a in opts:
				#print("o is now >%s<" % o)
				if o == "--objectName":
								objectName = a
				else:
								print("option %s not recognized " % o)


def showObjProp(objectName):
	print "removing files "
	os.system("rm -f listCenter-%s" % (objectName))
	os.system("rm -f listCenterAligned-%s" % (objectName))
	for ft in FILTERS:	
		print("start %s" % ft)
		with open(os.path.join(OUTPUTDIR, "object", ft, "list")) as file1:
			for line in file1:
				filename = os.path.join(OUTPUTDIR, "object", ft, line.strip())
				try:
					hdulist = pyfits.open(filename)
				except IOError as e:
					print "I/O error({0}): {1}".format(e.errno, e.strerror)
					continue		
				header = hdulist[0].header
				if(header["OBJECT"]==objectName):
						print("MATCH Filename abs path is %s "% filename)	
						os.system("echo %s >> listCenter-%s" % (filename, objectName))
						newfilename = filename[:-5] + "a" + ".fits"
						os.system("echo %s >> listCenterAligned-%s" % (newfilename, objectName))
					
	print "end showObjProp"

showObjProp(objectName)

 









