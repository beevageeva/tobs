import os, pyfits

from configLocal import OUTPUTDIR, FILTERS

calib_objects = ["pg2213", "pg2331", "pg0918", "pg0231"]


def showObjProp():
	print "start showObjProp"
	for ft in FILTERS:	
		print("start %s" % ft)
		with open(os.path.join(OUTPUTDIR, "object", ft, "list")) as file1:
			for line in file1:
				filename = line.strip()
				fitsfile = os.path.join(OUTPUTDIR, "object", ft, filename)	
				headerObjval = None
				try:
					hdulist = pyfits.open(fitsfile)
					headerObjval = hdulist[0].header["OBJECT"].lower()
				except Exception as e:
					print("Error :")
					print(e)
					continue
				calibObj = None
				if headerObjval:
					for co in calib_objects:
						if  co in headerObjval:
							calibObj = co
							break
				if calibObj:	
					newfitsfile = fitsfile[:-5] + "a" + ".fits"
					print("Adding to list %s , %s " % (fitsfile, newfitsfile) )
					os.system("echo %s >> listCenter-%s" %  (fitsfile, calibObj))
					os.system("echo %s >> listCenterAligned-%s" %  (newfitsfile, calibObj))
					
	print "end showObjProp"

showObjProp()

 









