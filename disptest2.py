import pyfits, pylab,sys, ds9
from pyraf import iraf

def displayImage(fitsfile):

	hl = pyfits.open(fitsfile)
	print("hdulist info")
	d.set_pyfits(hl)

	#im = pyfits.getdata(fitsfile)
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
	d.set('saveimage png %s.png' % fitsfile)
	data = hl[0].data
	maxv = 0
	cols = hl[0].columns
	print("column names")
	print(cols.names)
	



# Now open ds9 (this assumes no ds9 instance is yet running)
d = ds9.ds9()

iraf.display.setParam("frame", "1" )
iraf.display.setParam("erase", "yes" )
#iraf.display.image.p_mode = "h"
#iraf.display.frame.p_mode = "h"
displayImage(sys.argv[1])
