import os, shutil, re
from pyraf import iraf
from glob import glob
import numpy as np

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
#iraf.noao.imred.ccdred(Stdout=1)
iraf.noao.imred.bias(Stdout=1)

from configLocal import IMGDIR, OUTPUTDIR, FILTERS

BIAS_SEC= "[1025:1056,1:1024]"
DATA_SEC= "[1:1024,1:1024]"


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
		iraf.hselect.setParam("fields", "$I,OBJECT,ZD,RA,DEC,EXPTIME,AIRMASS,UT")
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


#TODO hselect not working
def initDirsNotWorking():
	for f in FILTERS:
		#flat
		fdir = 	os.path.join(OUTPUTDIR, "flat", f)
		createDir(fdir)
		#object
		fdir = 	os.path.join(OUTPUTDIR, "object", f)
		createDir(fdir)
	iraf.hselect.setParam("fields", "$I")
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
		
def initDirs():
	import pyfits,glob	
	for f in FILTERS:
		#flat
		fdir = 	os.path.join(OUTPUTDIR, "flat", f)
		createDir(fdir)
		#object
		fdir = 	os.path.join(OUTPUTDIR, "object", f)
		createDir(fdir)
	for fitsfile in glob.glob("%s/*.fits" % IMGDIR):
		try:
			hdulist = pyfits.open(fitsfile)
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			continue		
		header = hdulist[0].header
		#in M37 IMAGETYP = object for all
		#objectType = header["IMAGETYP"]
		if(header["OBJECT"].startswith("flat")):
			objectType = "flat"
		else:
			objectType = "object"		
		insfilter =  header["INSFILTE"]
		if insfilter in FILTERS:
			shutil.copy(fitsfile, os.path.join(OUTPUTDIR, objectType, insfilter))
			os.system("echo %s >> %s" % (os.path.basename(fitsfile), os.path.join(OUTPUTDIR, objectType, insfilter, "list" )))


def getFitsFileList(expr):
	from glob import glob 
	return glob.glob(expr).join(",")



def trimAndOverscan():
	print "TrimAndOverscan start"
#	#put all others params to no , they may be set by previous actions
#	iraf.ccdproc.setParam('instrum', '')
#	iraf.ccdproc.setParam('zerocor', 'no')
#	iraf.ccdproc.setParam('flatcor', 'no')
#	iraf.ccdproc.setParam('fixpix', 'no')
#	iraf.ccdproc.setParam('darkcor', 'no')
#	iraf.ccdproc.setParam('illumcor', 'no')
#	#trim and overscan flat and object files
#	iraf.ccdproc.setParam('trim', 'yes')
#	iraf.ccdproc.setParam('trimsec', DATA_SEC)
#	iraf.ccdproc.setParam('overscan', 'yes')
#	iraf.ccdproc.setParam('biassec', BIAS_SEC)
#	#online
#	iraf.ccdproc.setParam('output', '')

	#COLBIAS
	iraf.colbias.unlearn()
	iraf.colbias.setParam('bias', BIAS_SEC)
	iraf.colbias.setParam('trim', DATA_SEC)
	iraf.colbias.setParam("median", "no")
	iraf.colbias.setParam("interactive", "no")

	for imgtype in ["flat", "object"]:
		for f in FILTERS:
			#iraf.ccdproc.setParam("images", os.path.join(OUTPUTDIR, imgtype, f) + "/*.fits")
			#iraf.ccdproc()
			#COLBIAS
#			#list does not work
#			os.chdir(os.path.join(OUTPUTDIR, imgtype, f))
#			print("Current directory = %s" % os.getcwd())
#			import subprocess
#			outputPwd = subprocess.Popen('pwd', stdout=subprocess.PIPE).stdout.read()
#			print("outPwd = %s" % outputPwd)
#			#set it again
#			iraf.colbias.setParam('input',  "@list")
#			iraf.colbias.setParam('output', "@list")
#			iraf.colbias()
#			#end list
			#one by one
			with open(os.path.join(OUTPUTDIR, imgtype, f, "list")) as file1:
				for line in file1:
					filename = line.strip()
					if filename!="":
						print("Colbias %s " % os.path.join(OUTPUTDIR, imgtype, f, filename) )
#						iraf.colbias.setParam('input',  os.path.join(OUTPUTDIR, imgtype, f, filename))
#						iraf.colbias.setParam('output', os.path.join(OUTPUTDIR, imgtype, f, filename))
#						iraf.colbias()
						iraf.colbias(os.path.join(OUTPUTDIR, imgtype, f, filename), os.path.join(OUTPUTDIR, imgtype, f, filename))


	print "TrimAndOverscan end"




def createFlatFiles():
	import re
	print "CreateFlatFiles start"
	for f in FILTERS:
		if(os.listdir(os.path.join(OUTPUTDIR, "flat", f))):
			iraf.imcombine.setParam("input", os.path.join(OUTPUTDIR, "flat", f) + "/*.fits")
			flatFile = os.path.join(OUTPUTDIR, "flat", f , "Flat.fits")
			if os.path.exists(flatFile):
				print("flatFile %s alreday exists deleting"  % flatFile)
				os.remove(flatFile)
			iraf.imcombine.setParam("output", flatFile)
			#from doc:	
			#http://www.iac.es/sieinvens/siepedia/pmwiki.php?n=HOWTOs.PythonianIRAF
			#--> iraf.listpix(mode='ql')     # confirms parameter
			#--> iraf.listpix(mode='h')     # doesn't ask for parameter...@@
			iraf.imcombine(mode="h")
			#NORMALIZE
			#imstat
			res = iraf.imstat(flatFile, Stdout=1)
			print(res[0].strip()) 
			print(res[1].strip()) 
			resArray = re.split("\s+", res[1].strip())
			#max value
			#toDivValue = float(resArray[5])
			#meanValue
			toDivValue = float(resArray[2])
			flatNormFile = os.path.join(OUTPUTDIR, "flat", f , "FlatNorm.fits")
			if os.path.exists(flatNormFile):
				print("flatNormFile %s alreday exists deleting"  % flatNormFile)
				os.remove(flatNormFile)
			#divide by max value
			iraf.imarith(flatFile, '/', toDivValue, flatNormFile)
		else:
			print("NO FLAT FILES for filter %s PRESENT" %f)
	print "CreateFlatFiles end"



def flatCorrection():
	print "FlatCorrection start"
	#put all others params to no , they may be set by previous actions
	#WITH ccdproc
#	iraf.ccdproc.setParam('flatcor', 'yes')
#	iraf.ccdproc.setParam('fixpix', 'no')
#	iraf.ccdproc.setParam('darkcor', 'no')
#	iraf.ccdproc.setParam('illumcor', 'no')
#	iraf.ccdproc.setParam('trim', 'no')
#	iraf.ccdproc.setParam('overscan', 'no')
#	iraf.ccdproc.setParam('zerocor', 'no')
#	iraf.ccdproc.setParam('trimsec', '')
#	iraf.ccdproc.setParam('biassec', '')
#	#online
#	iraf.ccdproc.setParam('output', '')
	for f in FILTERS:	
		flatfilename = os.path.join(OUTPUTDIR, "flat", f, "FlatNorm.fits")
		if os.path.isfile(flatfilename):
#			#WITH ccdproc
#			iraf.ccdproc.setParam('flat', flatfilename)
#			iraf.ccdproc.setParam("images", os.path.join(OUTPUTDIR, "object", f) + "/*.fits")
#			iraf.ccdproc()
			with open(os.path.join(OUTPUTDIR, "object", f, "list")) as file1:
				for line in file1:
					objfilename = line.strip()
					if objfilename!="":
						objFullfilename = os.path.join(OUTPUTDIR, "object", f,	line.strip())
						iraf.imarith(objFullfilename, '/', flatfilename, objFullfilename)
		else:
			print "Flat file %s not present" % flatfilename
	print "FlatCorrection end"


#showImageProperties()
#initDirs()
#IMAGE CORRECTION
#trimAndOverscan()
#createFlatFiles()
#flatCorrection() 

#showFlatProp()
showObjProp()


#createBadPixelsMaskFiles()
#fixBadPixels()
#END IMAGE CORRECTION

#showObjProp()
#showTimeConv()
	

 









