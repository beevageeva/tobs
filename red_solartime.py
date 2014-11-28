import os, shutil
from pyraf import iraf

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.ccdred(Stdout=1)

IMGDIR = "/net/rusia/scratch/TecnicasOb/Nov1/" 
#OUTPUTDIR = os.path.join(IMGDIR , "out")
OUTPUTDIR = "/scratch/img112/"

FILTERS = ["R", "V", "I", "B", "U"]
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
	for r in iraf.hselect(Stdout=1):
		print r
	print "end"

	

def showObjProp(ft):
	print "start"
	print "object\tzenith dist\tright asc\tdecl"
	iraf.hselect.setParam("images", os.path.join(OUTPUTDIR, "object", ft) + "/*.fits")
	iraf.hselect.setParam("fields", "OBJECT,ZD,RA,DEC")
	iraf.hselect.setParam("expr", 'yes')
	print "start"
	for r in iraf.hselect(Stdout=1):
		print r
	print "end"



#TIME
def timeToSec(strTime):
	parts = strTime.split(":")
	if(len(parts)==3):
		res = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
		return res
	else:
		print("converting %s to seconds, len(parts) separated by : !=3, return 0" % strTime)
		return 0


def dif(s1, s2):
	si = []
	for s in [s1, s2]:
		si.append(s.split(":"))
	res = ""
	try:
		for i in range(0,3):
			res+=str(int(si[0][i]) - int(si[1][i]))
			if(i<2):
				res+=":"
	except ValueError:
		print("parts are not int s1=%s, s2=%s"%(s1,s2))
		return "00:00:00"
	return res	



#from http://stackoverflow.com/questions/13314626/local-solar-time-function-from-utc-and-longitude
from datetime import datetime, time, timedelta
from math import pi, sin, cos, atan2, asin

# helpful constant
DEG_TO_RAD = pi / 180

# hardcode difference between Dynamical Time and Universal Time
# delta_T = TD - UT
# This comes from IERS Bulletin A
# ftp://maia.usno.navy.mil/ser7/ser7.dat
DELTA = 35.0

def coords(yr, mon, day):
    # @input year (int)
    # @input month (int)
    # @input day (float)
    # @output right ascention, in radians (float)
    # @output declination, in radians (float)

    # get julian day (AA ch7)
    day += DELTA / 60 / 60 / 24 # use dynamical time
    if mon <= 2:
        yr -= 1
        mon += 12
    a = yr / 100
    b = 2 - a + a / 4
    jd = int(365.25 * (yr + 4716)) + int(30.6 * (mon + 1)) + day + b - 1524.5

    # get sidereal time at greenwich (AA ch12)
    t = (jd - 2451545.0) / 36525

    # Calculate mean equinox of date (degrees)
    l = 280.46646 + 36000.76983 * t + 0.0003032 * t**2
    while (l > 360):
        l -= 360
    while (l < 0):
        l += 360

    # Calculate mean anomoly of sun (degrees)
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t**2

    # Calculate eccentricity of Earth's orbit
    e = 0.016708634 - 0.000042037 * t - 0.0000001267 * t**2

    # Calculate sun's equation of center (degrees)
    c = (1.914602 - 0.004817 * t - .000014 * t**2) * sin(m * DEG_TO_RAD) \
        + (0.019993 - .000101 * t) * sin(2 * m * DEG_TO_RAD) \
        + 0.000289 * sin(3 * m * DEG_TO_RAD)

    # Calculate the sun's radius vector (AU)
    o = l + c # sun's true longitude (degrees)
    v = m + c # sun's true anomoly (degrees)

    r = (1.000001018 * (1 - e**2)) / (1 + e * cos(v * DEG_TO_RAD))

    # Calculate right ascension & declination
    seconds = 21.448 - t * (46.8150 + t * (0.00059 - t * 0.001813))
    e0 = 23 + (26 + (seconds / 60)) / 60

    ra = atan2(cos(e0 * DEG_TO_RAD) * sin(o * DEG_TO_RAD), cos(o * DEG_TO_RAD)) # (radians)
    decl = asin(sin(e0 * DEG_TO_RAD) * sin(o * DEG_TO_RAD)) # (radians)

    return ra, decl

def hour_angle(dt, longit):
    # @input UTC time (datetime)
    # @input longitude (float, negative west of Greenwich)
    # @output hour angle, in degrees (float)

    # get gregorian time including fractional day
    y = dt.year
    m = dt.month
    d = dt.day + ((dt.second / 60.0 + dt.minute) / 60 + dt.hour) / 24.0 

    # get right ascention
    ra, _ = coords(y, m, d)

    # get julian day (AA ch7)
    if m <= 2:
        y -= 1
        m += 12
    a = y / 100
    b = 2 - a + a / 4
    jd = int(365.25 * (y + 4716)) + int(30.6 * (m + 1)) + d + b - 1524.5

    # get sidereal time at greenwich (AA ch12)
    t = (jd - 2451545.0) / 36525
    theta = 280.46061837 + 360.98564736629 * (jd - 2451545) \
            + .000387933 * t**2 - t**3 / 38710000

    # hour angle (AA ch13)
    ha = (theta + longit - ra / DEG_TO_RAD) % 360

    return ha

def solarTime(datestr, timestr, longit):
    dt = datetime.strptime(datestr + ' ' + timestr, '%Y-%m-%d %H:%M:%S')
    ha = hour_angle(dt, longit)
    # convert hour angle to timedelta from noon
    days = ha / 360
    if days > 0.5:
        days -= 0.5
    td = timedelta(days=days)
    # make solar time
    solar_time = datetime.combine(dt.date(), time(12)) + td
    return solar_time

#http://www.eaae-astronomy.org/WG3-SS/WorkShops/LongLatOneStar.html





def showTimeConv():
	iraf.hselect.setParam("images", IMGDIR + "*.fits")
	iraf.hselect.setParam("fields", "OBJECT,ST,UT,INSFILTE,DATE-OBS")
	iraf.hselect.setParam("expr", 'yes')
	print "start"
	longit = 0.27925
	for rstr in iraf.hselect(Stdout=1, mode="h"):
		r = rstr.split("\t")
		#ST - UT - RA
		print r[0] +"\t"+ r[1] + "\t" + r[2] + "\t" + r[3] + "\t" + str(timeToSec(r[1]) - timeToSec(r[2])) +"\t"+ solarTime(r[4], r[2], longit).strftime("%Y-%m-%d %H:%M:%S")
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
#END IMAGE CORRECTION

#for f in FILTERS:	
#	showObjProp(f)
showTimeConv()

	

 









