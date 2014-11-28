import os, glob, shutil,sys
import matplotlib
matplotlib.use('TkAgg')
#from pyraf import iraf
## Initialize IRAF with ccdred
#iraf.noao.imred(Stdout=1)
#iraf.noao.imred.ccdred(Stdout=1)
import matplotlib.pyplot as plt 
import pyfits,numpy




IMG_DIR="/home/bpb/asign/tobs/img/"
IMG_TYPES = ['bias', 'flat', 'object']
FILTER_TYPES = ['R', 'V', 'I']



def displayImage(fitsfile):
	#following niot working with LEVELE1
	im = pyfits.getdata(fitsfile)
	#try
	hdu_list = pyfits.open(fitsfile)
	print(hdu_list.__len__())
	hdu = hdu_list[1].data
	print("HEADER")
	print(hdu_list[1].header)
	print(hdu_list[1].header['BITPIX'])

	#im = numpy.column_stack((hdu.field('PIXEL1'), hdu.field('PIXEL2'),hdu.field('PIXEL3'),hdu.field('PIXEL4') ,hdu.field('PIXEL5') ,hdu.field('PIXEL6') ,hdu.field('PIXEL7') ,hdu.field('PIXEL8') ,hdu.field('PIXEL9') ,hdu.field('PIXEL10') ,hdu.field('PIXEL11') ,hdu.field('PIXEL12') ,hdu.field('PIXEL13') ,hdu.field('PIXEL14') ,hdu.field('PIXEL15') ,hdu.field('PIXEL16')   ))

	im = hdu.field('SOLAR_CT')

	print("DATA TYPE" )
	print(im)
	print(type(im))
	print(dir(im))
	#print(type(im.imag))



	#numdisplay.display(im)
	#iraf.display(fitsfile)
	#plt.imshow(im,  aspect='equal')
	plt.imshow(im, extent=[100,0,0,1], aspect='auto')
	plt.title('Blue = J, Green = H, Red = K')
	plt.draw()
	plt.show()
	import time
	time.sleep(10)



def selectImageFiles():
	iraf.hselect.setParam("images", IMG_DIR+"*.fits")
	iraf.hselect.setParam("fields", "$I")
	for ft in FILTER_TYPES:
		ftdir = os.path.join(OUTPUT_DIR, ft)
		if not os.path.exists(ftdir):
			os.mkdir(ftdir)
		for imt in ['flat', 'object']:
			exprcond="INSFILTE==\"%s\" && IMAGETYP==\"%s\"" % (ft,imt)
			ftTypedir = os.path.join(ftdir, imt)
			selectAndCopy(ftTypedir, exprcond)		
	exprcond="IMAGETYP==\"bias\"" 
	OUTPUT_DIR=IMG_DIR + "output/"
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)
	selectAndCopy(os.path.join(OUTPUT_DIR, 'bias'), exprcond)	


def selectAndCopy(ftTypedir, exprcond):	
	if  os.path.exists(ftTypedir):
		print("deleting folder and  contents %s" % ftTypedir)
		shutil.rmtree(ftTypedir)
	os.mkdir(ftTypedir)
	iraf.hselect.setParam("expr", "'" + exprcond + "'")
	for resfile in iraf.hselect(Stdout=1):
		displayImage(resfile);
		
		displayImage(os.path.join(ftTypedir, resfile))



#selectImageFiles()
displayImage(sys.argv[1])

 
