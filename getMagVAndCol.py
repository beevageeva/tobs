import getopt,sys, re,os , commands

extCor = False

try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["number=", "obj=" , "extcor"])
except getopt.GetoptError as err:
				# print help information and exit:
				print("Error in parsing args")
				print(str(err)) # will print something like "option -a not recognized"
				sys.exit(2)
objs=[]
numbers = []
for o, a in opts:
				if o == "--number":
								numbers = a.split(",")
				elif o == "--obj":
								objs = a.split(",")
				elif o == "--extcor":
								extCor = True
				else:
								print("option %s not recognized " % o)

from configLocal import OUTPUTDIR, FILTERS



files = ""
i = 0	
for o in objs:
	if len(numbers)==1:
		n = numbers[0]
	else:
		if len(numbers) > i:
			n = numbers[i]
		else:
			print("you are stupid")
			n = numbers[0]

	if extCor:
		fn = "RESOBJ_%s_CORR_EXT" % n
	else:
		fn = "RESOBJ_%s" % n
	files += os.path.join(OUTPUTDIR, "ALSREAD-%s" % o, fn) + " "  #USE corrected files
	i+=1		

import re

mag={}

for f in FILTERS:
	st, out = commands.getstatusoutput("cat %s | grep %s" % (files, f))
	sumVals=0
	nVals = 0
	for line in out.strip().split("\n"):
		vals = re.split("\s+", line)
		sumVals+=float(vals[2])
		nVals+=1
	mag[f] = sumVals/nVals

#print(mag)
#print("V B-V V-R")
print("%4.3f %4.3f %4.3f" % (mag['V'], mag['B'] - mag['V'], mag['V'] - mag['R'] ))
	

