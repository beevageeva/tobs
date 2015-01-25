import os, glob, shutil,sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import pyfits,numpy
import re

from configLocal import OUTPUTDIR

import matplotlib.colors 

def displayImage(fitsfile, mw, scale = False):
	try:
		hdulist = pyfits.open(fitsfile)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	header = hdulist[0].header
	im = hdulist[0].data
	if scale:
		numpy.seterr(over='ignore')
		if(header["INSFILTE"] == "V"):
			sc=2
		elif(header["INSFILTE"] == "B"):
			sc = 4
		else:
			sc = 1.6
		try: 
			im = sc ** im
		except Exception:
			#im = hdulist[0].data		
			print "OVERFOW"
	print("FITSfile = %s , coordfile = %s MIN=%e,MAX=%e" % (fitsfile, mw,im.min(), im.max()))
	plt.cla()
	plt.title(fitsfile)		
	#plt.imshow(im, cmap='gray',origin='lower', interpolation='nearest', clim=(100,4000))
	plt.imshow(im, cmap='gray')
	#plt.imshow(im, cmap='gray', norm=matplotlib.colors.LogNorm(0,1))
	n = 0
	nput=0
	with open(mw) as file2:
		for line2 in file2:
			coords = re.split('\s+', line2.strip())
			text = coords[2]
			print("New star %s n = %d nput = %d" % (text, n , nput))
			xc = float(coords[0])
			yc = float(coords[1])
			if nput<markNumber:
				if not str(n) in excluded:
					plt.annotate(text, fontsize=10, xy=(xc, yc),
	            xycoords='data', xytext=(xc-60, yc-60),
	            textcoords='data', color='red',
	            arrowprops=dict(arrowstyle="->",
	                            linewidth = 1.,
	                            color = 'red')
	            )
					nput+=1
				else:
					print("EXCLUDING %d" %n)
			n+=1
	directory = os.path.join(os.path.dirname(fitsfile), header["object"]+"CHARTS")
	if not os.path.exists(directory):
		os.makedirs(directory)
	newfile = os.path.join(directory, os.path.basename(fitsfile)+".png")
	print("Saving as %s " % newfile)
	os.system("rm -f %s" % newfile)		
	plt.savefig(newfile)	


import getopt,sys, re
try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["listFiles=", "markNumber=", "excluded=", "scale"])
except getopt.GetoptError as err:
				# print help information and exit:
				print("Error in parsing args")
				print(str(err)) # will print something like "option -a not recognized"
				sys.exit(2)
#print("OPTIONS")
#print(opts)
#print("OPTIONS END")
listFiles = None
markNumber = 10
excluded=[]
scale = False
for o, a in opts:
				#print("o is now >%s<" % o)
				if o == "--listFiles":
								listFiles = a
				if o == "--markNumber":
								markNumber = a
				if o == "--excluded":
								excluded = a.split(",")
				if o == "--scale":
								scale = True
				else:
								print("option %s not recognized " % o)


prefMark = "RESMARK"
print("FROM LISTFILE %s" %listFiles)
print("EXCLUDING:")
for x in excluded:
	print "EXc %s " % x	
with open(listFiles) as file1:
	for line in file1:
		fn = line.strip()
		mw = os.path.join(os.path.dirname(fn), "%s_%s" % (prefMark,os.path.basename(fn) ))	
		displayImage(fn,mw, scale)	


 
