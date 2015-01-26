import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import re,os,commands,sys

from configLocal import OUTPUTDIR, FILTERS

extCor = False


#Av + (b0-v0) * Bv = V- v0
#Abv + (b0 - v0) * Bbv = B -V
#Avr + (v0 - r0) * Bvr = V -R

def makeCalib():
	fnStd = "STANDARD"
	fnLoc = "OUT"
	
	coef = []
	
	
	V, BV, VR = np.loadtxt(fnStd, unpack = True)
	v0, b0v0, v0r0 = np.loadtxt(fnLoc, unpack = True)
	
	N = V.shape[0]
	
	print(N)
	
	print("V=")
	print(b0v0)
	
	A1 = np.dstack((np.ones(N), b0v0))[0]
	b1 = V - v0
	print("Matrix")
	print(A1.shape)
	print(A1)
	print("b")
	print(b1.shape)
	print(b1)
	
	coef.extend( np.linalg.lstsq(A1,b1)[0])
	coef.extend( np.linalg.lstsq( np.dstack((np.ones(N), b0v0))[0] , BV  )[0])
	coef.extend( np.linalg.lstsq( np.dstack((np.ones(N), v0r0))[0] , VR  )[0])
	
	print coef
	return coef



def calibAll(objName, coef):
	
	from glob import glob
	
	N = 10
	n = 0
	while n<10:
		newfilename =  os.path.join(OUTPUTDIR, "ALSREAD-%s" % objName, "RES_OBJ_%d_AVG_CORR_STD" % n)  
		if os.path.exists(newfilename):
			os.remove(newfilename)
		newfile = open(newfilename, "w")
		if extCor:
			cmd = "python getMagVAndCol.py --obj=%s --number=%d --extcor" % (objName, n)
		else:
			cmd = "python getMagVAndCol.py --obj=%s --number=%d" % (objName, n)	
		status, output =  commands.getstatusoutput(cmd)
		#print(output)
		gg =  output.strip().split("\n")
		vals = re.split("\s+", gg[-1])
		print(vals)
		if len(vals)<3:
			print("len < 3 for obj=%s number=%d" % (objName, n) )
			continue	
		v0 = float(vals[0])
		b0v0 = float(vals[1])	
		v0r0 = float(vals[2])
		newv0 = v0 + coef[0] + coef[1] * b0v0
		newb0v0 = coef[2] + coef[3] * b0v0
		newv0r0 = coef[4] + coef[5] * v0r0		
		newfile.write("%4.3f %4.3f %4.3f " % (newv0, newb0v0, newv0r0 ))
		newfile.close()
		n+=1

coefCorr = makeCalib()
calibAll("M37", coefCorr)
calibAll("pg2213_2", coefCorr)
calibAll("pg2213", coefCorr)
calibAll("pg2331", coefCorr)
calibAll("pg0918", coefCorr)
calibAll("pg0231", coefCorr)
calibAll("pg0231_2", coefCorr)



