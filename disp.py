import os, glob, shutil,sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import pyfits,numpy
import re




def displayImage(fitsfile):
	im = pyfits.getdata(fitsfile)
	print("shape of im")
	print(im.shape)	
	plt.imshow(im, cmap='gray',origin='lower')
	plt.draw()
	plt.show(block=True)	


def display2Images(fits1, fits2):
	fig = plt.figure(1)
	ax1= fig.add_subplot(1, 2, 1)
	ax2= fig.add_subplot(1, 2, 2)
	ax1.imshow(pyfits.getdata(fits1), cmap="gray")
	ax2.imshow(pyfits.getdata(fits2), cmap="gray")
	plt.draw()
	plt.show(block=True)	


if(len(sys.argv)==2):
	displayImage(sys.argv[1])
elif (len(sys.argv)==3):
	display2Images(sys.argv[1], sys.argv[2])

 
