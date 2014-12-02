import os, glob, shutil,sys
import pyfits,numpy
import re




def displayImage(fitsfile):
	im = pyfits.getdata(fitsfile)
	print("shape of im")
	print(im.shape)	
	print("data")
	print(im)


displayImage(sys.argv[1])

 
