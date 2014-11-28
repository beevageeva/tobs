import pyfits, pylab,sys, ds9
from pyraf import iraf
import numpy as np

def displayImage(fitsfile):

	#print "imsize %d " % len(im)
	#d.set_np2arr(im)
	 
	# Zoom to fit
	#d.set('zoom to fit')
	 
	# Change the colormap and scaling
	#d.set('cmap bb')
	#d.set('scale log')
	 
	# Add a label
	#d.set('regions command {text 30 20 #text="Fun with pyds9" font="times 18 bold"}')
	 
	# Now you can play in ds9 to your heart's content.
	# Check back to see what the current color scale is.
	#print d.get('scale')
	 
	# Finally, save your completed image (including regions or labels)
	iraf.daofind.setParam("findpars", "findpars.txt")
	iraf.daofind(fitsfile)
	



# Now open ds9 (this assumes no ds9 instance is yet running)
displayImage(sys.argv[1])
