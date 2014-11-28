import os, shutil, re
from pyraf import iraf
from glob import glob
import numpy as np

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.ccdred(Stdout=1)

IMGDIR = "/net/rusia/scratch/TecnicasOb/Nov1/" 
#OUTPUTDIR = os.path.join(IMGDIR , "out")
OUTPUTDIR = "/scratch/img112/"

FILTERS = ["R", "V", "I", "B", "U"]
BIAS_SEC= "[1025:1056,1:1024]"
DATA_SEC= "[1:1024,1:1024]"

star_pos = {"M37":{'dec': '32:00:00'}, "RU149":{"ra":"07:24:13"	, 'dec':"-00:31:58"}	 }

def createDir(folder):
	if os.path.exists(folder):
		shutil.rmtree(folder)
	os.makedirs(folder)




def showImageProperties():
	iraf.hselect.setParam("images", IMGDIR + "*.fits")
	iraf.hselect.setParam("fields", "$I, IMAGETYP, INSFILTE, BIASSEC, DATASEC")
	iraf.hselect.setParam("expr", 'yes')
	print "start"
	print "filename\ttype\tfilter\tbiassec\tdatasec"
	for r in iraf.hselect(Stdout=1, mode="h"):
		print r
	print "end"

	

def showObjProp():
	print "start showObjProp"
	for ft in FILTERS:	
		print("start %s" % ft)
		print "object\tzenith dist\tright asc\tdecl\texptime\tairmass\tUT"
		iraf.hselect.setParam("images", os.path.join(OUTPUTDIR, "object", ft) + "/*.fits")
		iraf.hselect.setParam("fields", "OBJECT,ZD,RA,DEC,EXPTIME,AIRMASS,UT")
		iraf.hselect.setParam("expr", 'yes')
		for r in iraf.hselect(Stdout=1, mode="h"):
			print r
	print "end showObjProp"


def showFlatProp():
	print "start showFlatProp"
	for ft in FILTERS:	
		print("start %s" % ft)
		print "object\texptime"
		iraf.hselect.setParam("images", os.path.join(OUTPUTDIR, "flat", ft) + "/*.fits")
		iraf.hselect.setParam("fields", "$I,OBJECT,EXPTIME")
		iraf.hselect.setParam("expr", 'yes')
		for r in iraf.hselect(Stdout=1, mode="h"):
			print r
	print "end showFlatProp"

#TIME
def timeToSec(strTime):
	parts = strTime.split(":")
	if(len(parts)==3):
		res = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
		return res
	else:
		print("converting %s to seconds, len(parts) separated by : !=3, return 0" % strTime)
		return 0



def binOp(s1,s2,binFunc):
	si = []
	for s in [s1, s2]:
		s = re.sub("[ \"]", "", s)
		parts = s.split(":")
		if(len(parts)!=3):
			print("len parts !=3 for string %s return 00:00:00" % s)
			return "00:00:00"	
		si.append(parts)
	res = ""
	try:
		for i in range(0,3):
			res+=str(binFunc(int(si[0][i]), int(si[1][i] ))) #for the moment only here
			if(i<2):
				res+=":"
	except ValueError:
		print("parts are not int s1=%s, s2=%s"%(s1,s2))
		return "00:00:00"
	return res	


def sdif(s1, s2):
	return binOp(s1,s2, lambda x, y: x - y)
	

def ssum(s1, s2):
	return binOp(s1,s2, lambda x, y: x + y)

#if firstNeg will output first part negative if it's bigger than half of max value
def positiveString(s, maxvals, firstNeg = False):
	parts = s.split(":")
	if(len(parts)!=3):
			print("len parts separated by : !=3 for string %s return 00:00:00" % s)
			return "00:00:00"	
	res = ""
	try:
		fromlast = 0
		for i in range(2,-1,-1):
			val = int(parts[i])
			val+=fromlast
			fromlast = 0
			while(val<0):
				val+=maxvals[i]
				fromlast-=1
			while(val>=maxvals[i]):
				val-=maxvals[i]
				fromlast+=1
			res = str(val)+ res
			if(i>0):
				res = ":" + res
	except ValueError:
		print("parts are not int %s" % s)
		return "00:00:00"
	if(firstNeg):
		parts = res.split(":")
		if(int(parts[0]) > maxvals[0] * 0.5):
			res = "-" + str(maxvals[0] - 1 - int(parts[0])) + ":" +  str(maxvals[1] - int(parts[1])) + ":" +  str(maxvals[2] - int(parts[2]))
	return res	

def hourFormatPositive(s):
	return positiveString(s, [24,60,60])

def angleFormatPositive(s, firstNeg = False):
	return positiveString(s, [360,60,60], firstNeg)

def hoursToDegreesFormat(s, firstNeg = False):
	parts = s.split(":")
	if(len(parts)!=3):
			print("len parts separated by : !=3 for string %s return 00:00:00" % s)
			return "00:00:00"	
	res = ""
	try:
		for i in range(0,3):
			val = int(parts[i]) * 15 #15 = 360/24
			res+=str(val)	
			if(i<2):
				res+=":"
	except ValueError:
		print("parts are not int s=%s"%s)
		return "00:00:00"
	return angleFormatPositive(res, firstNeg)	




def showTimeConv():
	iraf.hselect.setParam("images", IMGDIR + "*.fits")
	iraf.hselect.setParam("fields", "OBJECT,ST,UT,INSFILTE,DATE-OBS,RA,ZD,DEC")
	iraf.hselect.setParam("expr", 'yes')
	print "start"
	#print "object\tst\tut\tra\t(st-ut-ra)"
	print "object\tst\tut\tut(Deg)\tra\t(st-ut)Hours\t(st-ut)Deg\tzd\tdec\t(zd+dec)"
	longit = 0.27925
	for rstr in iraf.hselect(Stdout=1, mode="h"):
		r = rstr.split("\t")
		#ST - UT - RA
		#print r[0] +"\t"+ r[1] + "\t" + r[2] + "\t" + r[3] + "\t" + r[5] + "\t" +  dif(dif(r[1],r[2]),r[5])
		timeDif = sdif(r[1],r[2])
		print(r[0] +"\t"+ r[1] + "\t" + r[2] + "\t" + hoursToDegreesFormat(r[2],True)+ "\t" + r[5] + "\t" +  hourFormatPositive(timeDif)+ "\t" + hoursToDegreesFormat(timeDif, True) + "\t"+ r[6] + "\t" + r[7]+ "\t"+ angleFormatPositive(ssum(r[6],r[7])))
	print "end"




#END TIME



def initDirs():
	#bias
	createDir(os.path.join(OUTPUTDIR, "bias"))
	for f in FILTERS:
		#flat
		fdir = 	os.path.join(OUTPUTDIR, "flat", f)
		createDir(fdir)
		#object
		fdir = 	os.path.join(OUTPUTDIR, "object", f)
		createDir(fdir)
	iraf.hselect.setParam("fields", "$I")
	#copy bias files
	iraf.hselect.setParam("images", IMGDIR + "*.fits")
	iraf.hselect.setParam("expr", 'IMAGETYP=="bias"')
	for imgname in iraf.hselect(Stdout=1):
		shutil.copy(imgname, os.path.join(OUTPUTDIR, "bias"))
	for f in FILTERS:
		#copy flat files	
		iraf.hselect.setParam("expr", 'IMAGETYP=="flat"&&INSFILTE=="%s"' % f)
		for imgname in iraf.hselect(Stdout=1):
			print("imgname to copy for flat files and filter %s is %s" % (f, imgname))
			shutil.copy(imgname, os.path.join(OUTPUTDIR, "flat", f))
		#copy object files	
		iraf.hselect.setParam("expr", 'IMAGETYP=="object"&&INSFILTE=="%s"' % f)
		for imgname in iraf.hselect(Stdout=1):
			shutil.copy(imgname, os.path.join(OUTPUTDIR, "object", f))
		
def trimAndOverscan():
	print "TrimAndOverscan start"
	#put all others params to no , they may be set by previous actions
	iraf.ccdproc.setParam('zerocor', 'no')
	iraf.ccdproc.setParam('flatcor', 'no')
	iraf.ccdproc.setParam('fixpix', 'no')
	iraf.ccdproc.setParam('darkcor', 'no')
	iraf.ccdproc.setParam('illumcor', 'no')
	#trim and overscan flat and object files
	iraf.ccdproc.setParam('trim', 'yes')
	iraf.ccdproc.setParam('trimsec', DATA_SEC)
	iraf.ccdproc.setParam('overscan', 'yes')
	iraf.ccdproc.setParam('biassec', BIAS_SEC)
	#online
	iraf.ccdproc.setParam('output', '')
	for imgtype in ["flat", "object"]:
		for f in FILTERS:
			iraf.ccdproc.setParam("images", os.path.join(OUTPUTDIR, imgtype, f) + "/*.fits")
			iraf.ccdproc()
	#only trim for bias files	
	if(os.listdir(os.path.join(OUTPUTDIR, "bias"))):
		iraf.ccdproc.setParam('overscan', 'no')
		iraf.ccdproc.setParam('biassec', '')
		iraf.hselect.setParam("images",   os.path.join(OUTPUTDIR, "bias") + "/*.fits")
		iraf.ccdproc()
	else:
		print "No Bias Files present"	
	print "TrimAndOverscan end"

def createZeroFile():
	print "CreateZeroFile start"
	if(os.listdir(os.path.join(OUTPUTDIR, "bias"))):
		iraf.imcombine.setParam("input", os.path.join(OUTPUTDIR, "bias") + "/*.fits")
		zeroFile = os.path.join(OUTPUTDIR, "bias", "Zero.fits")
		if os.path.exists(zeroFile):
			os.remove(zeroFile)
		iraf.imcombine.setParam("output", zeroFile)
		iraf.imcombine()
	else:
		print("NO BIAS FILES PRESENT")
	print "CreateZeroFile end"



# image param for ccdmask is the CCD image to use in defining bad pixels. Typically this is a flat field image or, even better, the ratio of two flat field images of different exposure levels.
def createBadPixelsMaskFiles():
	print "CreateBadPixelsMaskFiles start"
	for f in FILTERS:
		resFile = os.path.join(OUTPUTDIR, "flat", f, "minExpDivMaxExp.fits")
		maskFile = resFile[:-4]+ "mask"
		if os.path.exists(resFile):
			os.remove(resFile)	
		if os.path.exists(maskFile + ".pl"):
			os.remove(maskFile + ".pl")	
		fdir = 	os.path.join(OUTPUTDIR, "flat", f)
		iraf.hselect.setParam("images", fdir + "/Nov*.fits") #TODO because it's done after flat combine
		iraf.hselect.setParam("fields", "$I,EXPTIME")
		iraf.hselect.setParam("expr", 'yes')
		maxExpTime = 0
		minExpTime = np.inf
		minExpFlatFile = None
		maxExpFlatFile = None
		for rs in iraf.hselect(Stdout=1, mode="h"):
			r = rs.split("\t")
			print("image %s" % r[0])
			try:
				expTime = float(r[1])
			except ValueError:
				print("exptime not float %s, set to 1"%r[1])
				expTime = 1
			print("expTime %4.2f" % expTime)
			if(expTime<minExpTime):
				minExpTime = expTime
				minExpFlatFile = r[0]
			elif(expTime>maxExpTime):
				maxExpTime = expTime
				maxExpFlatFile = r[0]
		print("filter=%s minExpTime = %4.3f in flatfile = %s, maxExpTime = %4.3f in flatfile = %s "%(f,minExpTime, minExpFlatFile,maxExpTime, maxExpFlatFile))
		if not minExpFlatFile is None:
			#now divide the 2 images
			iraf.imarith.setParam("operand1", minExpFlatFile)	
			iraf.imarith.setParam("operand2", maxExpFlatFile)	
			iraf.imarith.setParam("op", "/")	
			iraf.imarith.setParam("result", resFile)
			iraf.imarith(Stdout=1, mode="h")	
			iraf.ccdmask.setParam("image", resFile)
			iraf.ccdmask.setParam("mask", maskFile)
			iraf.ccdmask(Stdout=1, mode="h")
	print "CreateBadPixelsMaskFiles end"



def fixBadPixels():
	print "FixBadPixels start"
	#for f in FILTERS:
	for f in ["V"]:
		maskfile = os.path.join(OUTPUTDIR, "flat", f, "minExpDivMaxExp.fits")[:-4] + "mask"
		#iraf.fixpix.setParam("images", os.path.join(OUTPUTDIR, "flat", f) + "/*.fits")	
		iraf.fixpix.setParam("images","/home/bpb/asign/tobs/pyraf/Nov010065.fits")	
		iraf.fixpix.setParam("masks", maskfile)	
		iraf.fixpix(Stdout=1, mode="h")
		#TODO  TRY THIS
		#iraf.ccdproc.setParam('fixpix', 'yes')
		#iraf.ccdproc.setParam('fixfile', maskfile)
#		iraf.ccdproc.setParam('zerocor', 'no')
#		iraf.ccdproc.setParam('flatcor', 'no')
#		iraf.ccdproc.setParam('fixpix', 'no')
#		iraf.ccdproc.setParam('darkcor', 'no')
#		iraf.ccdproc.setParam('illumcor', 'no')
#		iraf.ccdproc.setParam('trim', 'no')
#		iraf.ccdproc.setParam('overscan', 'no')
		
	print "FixBadPixels end"
		
		



def createFlatFiles():
	print "CreateFlatFiles start"
	for f in FILTERS:
		if(os.listdir(os.path.join(OUTPUTDIR, "flat", f))):
			iraf.imcombine.setParam("input", os.path.join(OUTPUTDIR, "flat", f) + "/*.fits")
			flatFile = os.path.join(OUTPUTDIR, "flat", f , "Flat.fits")
			if os.path.exists(flatFile):
				os.remove(flatFile)
			iraf.imcombine.setParam("output", flatFile)
			iraf.imcombine()
		else:
			print("NO FLAT FILES for filter %s PRESENT" %f)
	print "CreateFlatFiles end"


def zeroCorrection():
	print "ZeroCorrection start"
	#put all others params to no , they may be set by previous actions
	zerofilename = os.path.join(OUTPUTDIR, "bias",  "Zero.fits")
	if os.path.isfile(zerofilename):
		iraf.ccdproc.setParam('flatcor', 'no')
		iraf.ccdproc.setParam('fixpix', 'no')
		iraf.ccdproc.setParam('darkcor', 'no')
		iraf.ccdproc.setParam('illumcor', 'no')
		iraf.ccdproc.setParam('trim', 'no')
		iraf.ccdproc.setParam('overscan', 'no')
		#trim and overscan flat and object files
		iraf.ccdproc.setParam('zerocor', 'yes')
		iraf.ccdproc.setParam('zero', zerofilename)
		iraf.ccdproc.setParam('trimsec', '')
		iraf.ccdproc.setParam('biassec', '')
		#online
		iraf.ccdproc.setParam('output', '')
		for imgtype in ["flat", "object"]:
			for f in FILTERS:
				iraf.ccdproc.setParam("images", os.path.join(OUTPUTDIR, imgtype, f) + "/*.fits")
				iraf.ccdproc()
	else:	
		print "Zero file %s not present" % zerofilename
	print "ZeroCorrection end"

def flatCorrection():
	print "FlatCorrection start"
	#put all others params to no , they may be set by previous actions
	iraf.ccdproc.setParam('flatcor', 'yes')
	iraf.ccdproc.setParam('fixpix', 'no')
	iraf.ccdproc.setParam('darkcor', 'no')
	iraf.ccdproc.setParam('illumcor', 'no')
	iraf.ccdproc.setParam('trim', 'no')
	iraf.ccdproc.setParam('overscan', 'no')
	iraf.ccdproc.setParam('zerocor', 'no')
	iraf.ccdproc.setParam('trimsec', '')
	iraf.ccdproc.setParam('biassec', '')
	#online
	iraf.ccdproc.setParam('output', '')
	for f in FILTERS:	
		flatfilename = os.path.join(OUTPUTDIR, "flat", f, "Flat.fits")
		if os.path.isfile(flatfilename):
			iraf.ccdproc.setParam('flat', flatfilename)
			iraf.ccdproc.setParam("images", os.path.join(OUTPUTDIR, "object", f) + "/*.fits")
			iraf.ccdproc()
		else:
			print "Flat file %s not present" % flatfilename
	print "FlatCorrection end"


#showImageProperties()
#initDirs()
#IMAGE CORRECTION
#trimAndOverscan()
#createZeroFile()
#zeroCorrection()
#createFlatFiles()
#flatCorrection() 
#ILLUMINATION CORR
#showFlatProp()

#END ILLUMINATION CORR

#createBadPixelsMaskFiles()
fixBadPixels()
#END IMAGE CORRECTION

#showObjProp()
#showTimeConv()
	

 









