import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import re,os,commands,sys

from configLocal import OUTPUTDIR




def makeCalib(objName, calibStar):
	#funcCorr = {}
	coefCorr = {}
	with open(os.path.join(OUTPUTDIR, "ALSREAD-%s" % objName, "RESOBJ_%d" % calibStar)) as file1:
		xvals = {'R':[], 'V':[], 'B':[]}
		yvals = {'R':[], 'V':[], 'B':[]}
		for line1 in file1:
			line1=line1.strip()
			vals = re.split("\s+", line1)	
			mag = float(vals[2])
			fn = vals[3]
			indObj = fn.rindex("object/")
			filt = fn[indObj+7]
			status, output =  commands.getstatusoutput("python dispHeader.py %s | grep AIRMASS" % (fn))
			airmass = float(output.strip().split('=')[1].strip())
			os.system("echo %2.3f %2.3f >> %s" % (airmass, mag, "FIT_" + filt))
			xvals[filt].append(airmass)
			yvals[filt].append(mag)
			print(mag,filt,airmass)
	
	
	for filt in ['R', 'V', 'B']:
		#funcCorr[filt] = np.poly1d(np.polyfit(xvals[filt], yvals[filt], 1))
		coef= np.polyfit(xvals[filt], yvals[filt], 1)
		#coefCorr[filt] = 	-coef[1] / coef[0]	
		coefCorr[filt] = 	-coef[0] / coef[1]	
		print("Filter %s coef = %4.3f" % (filt, coefCorr[filt]))
	return coefCorr	


def calibAll(objName, coefCorr):
	
	from glob import glob
	
	N = 10
	for fn in  glob("%s/RESOBJ_*" % os.path.join(OUTPUTDIR, "ALSREAD-%s" % objName)):
		m = re.match('\S+RESOBJ_(\d+)$', fn)
		if m and int(m.group(1))<N:
			print("FN = %s" % fn)
			with open(fn) as file1:
				newfilename = fn+ "_CORR_EXT"
				if os.path.exists(newfilename):
					os.remove(newfilename)
				newfile = open(newfilename, "w")
				for line1 in file1:
					line1=line1.strip()
					if line1=="":
						continue
					vals = re.split("\s+", line1)	
					mag = float(vals[2])
					fn = vals[3]
					indObj = fn.rindex("object/")
					filt = fn[indObj+7]
					status, output =  commands.getstatusoutput("python dispHeader.py %s | grep AIRMASS" % (fn))
					airmass = float(output.strip().split('=')[1].strip())
					newmag = mag - coefCorr[filt] * airmass
					print("filter = %s , mag = %4.3f , newmag = %4.3f" % (filt, mag, newmag))
					newfile.write("%s %s %4.3f %s" % (vals[0], vals[1], newmag, fn ))
	
coefCorr = makeCalib("M37",0)
calibAll("M37", coefCorr)
calibAll("pg2213_2", coefCorr)
calibAll("pg2213", coefCorr)
calibAll("pg2331", coefCorr)
calibAll("pg0918", coefCorr)
calibAll("pg0231", coefCorr)
calibAll("pg0231_2", coefCorr)



