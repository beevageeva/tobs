import os, shutil, re
from pyraf import iraf
from glob import glob
import numpy as np

# Initialize IRAF with ccdred
iraf.noao.digiphot(Stdout=1)

from configLocal import IMGDIR, OUTPUTDIR, FILTERS


def showObjProp():
	print "start showObjProp"
	for ft in FILTERS:	
		print("start %s" % ft)
		with open(os.path.join(OUTPUTDIR, "object", ft, "list")) as file1:
			for line in file1:
				filename = line.strip()
				if filename!="":
					last3 = 0
					try:
						last3 = int(filename[-9:-5])
					except ValueError:
						print("not a number")
					if(last3>=96 and last3 <=105):
						newfilename = filename[:-5] + "a" + ".fits"
						print("Imalign %s to %s " % (filename,newfilename) )
						os.system("echo %s >> listCenter-M37" % os.path.join(OUTPUTDIR, "object", ft, filename))
						os.system("echo %s >> listCenterAligned-M37" % os.path.join(OUTPUTDIR, "object", ft, newfilename))
						#iraf.imalign(filename,"/scratch/M37New/object/V/Nov30098.fits","coords-98-aligned.txt", newfilename)
						#iraf.imalign.input=filename
						#iraf.imalign.reference=os.path.join(OUTPUTDIR, "object","V","Nov30098.fits")
						#iraf.imalign.coords="coords-98-aligned.txt"
						#iraf.imalign.output=newfilename
						#iraf.imalign.shifts=""
						
					
						#iraf.imalign(input=filename, reference="/scratch/M37New/object/V/Nov30098.fits", coords="coords-98-aligned.txt", output=newfilename, shifts="")
						#iraf.imalign()
					
	print "end showObjProp"

showObjProp()

 









