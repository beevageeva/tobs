import time, ds9, sys
from pyraf import iraf



saveImage = False

def displayImage(fitsfile):

 
	# Now open ds9 (this assumes no ds9 instance is yet running)
	d = ds9.ds9()

	iraf.display.setParam("image", fitsfile)
	iraf.display(mode="h")
	 
	if saveImage:
		# Zoom to fit
		d.set('zoom to fit')
		 
		# Change the colormap and scaling
		#d.set('cmap bb')
		#d.set('scale log')
		 
		# Add a label
		#d.set('regions command {text 30 20 #text="Fun with pyds9" font="times 18 bold"}')
		 
		# Now you can play in ds9 to your heart's content.
		# Check back to see what the current color scale is.
		#print d.get('scale')
		 
		# Finally, save your completed image (including regions or labels)
		d.set('saveimage png %s2.png' % fitsfile)
		d.pid.terminate()
		time.sleep(2)



iraf.display.setParam("frame", "1" )
iraf.display.setParam("erase", "yes" )
#iraf.display.image.p_mode = "h"
#iraf.display.frame.p_mode = "h"
if len(sys.argv) == 3:
	iraf.display.setParam("overlay", sys.argv[2])
else:
	iraf.display.setParam("overlay", '')
	

displayImage(sys.argv[1])
