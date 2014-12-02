from pyraf import iraf
from glob import glob
import numpy as np

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.bias(Stdout=1)
#iraf.noao.imred.ccdred(Stdout=1)

IMGDIR = "imagenesfits" 
OUTPUTDIR = "new"

BIAS_SEC= "[1025:1056,1:1024]"
DATA_SEC= "[1:1024,1:1024]"

def trimImages():
		iraf.colbias.unlearn() 
		iraf.colbias.setParam('bias', BIAS_SEC)
		iraf.colbias.setParam('trim', BIAS_SEC)
		iraf.colbias.setParam("median", "no")
		#iraf.colbias.setParam('input',   'imagenesfits/*.fits')
		#iraf.colbias.setParam('output', '')
	
		iraf.colbias.setParam("input",   "imagenesfits/FOct110001.imh.fits,imagenesfits/FOct110002.imh.fits,imagenesfits/FOct110003.imh.fits,imagenesfits/FOct110004.imh.fits,imagenesfits/FOct110005.imh.fits,imagenesfits/FOct110007.imh.fits,imagenesfits/FOct110008.imh.fits,imagenesfits/FOct110009.imh.fits,imagenesfits/FOct110010.imh.fits,imagenesfits/FOct110011.imh.fits,imagenesfits/FOct110012.imh.fits,imagenesfits/FOct110013.imh.fits,imagenesfits/FOct110014.imh.fits,imagenesfits/FOct110015.imh.fits,imagenesfits/FOct110016.imh.fits,imagenesfits/FOct110017.imh.fits,imagenesfits/FOct110018.imh.fits,imagenesfits/FOct110019.imh.fits,imagenesfits/FOct110020.imh.fits,imagenesfits/FOct110022.imh.fits,imagenesfits/FOct110023.imh.fits,imagenesfits/FOct110024.imh.fits,imagenesfits/FOct110025.imh.fits,imagenesfits/FOct110026.imh.fits,imagenesfits/FOct110027.imh.fits,imagenesfits/FOct110028.imh.fits,imagenesfits/FOct110029.imh.fits,imagenesfits/FOct110030.imh.fits,imagenesfits/FOct110031.imh.fits,imagenesfits/FOct110032.imh.fits,imagenesfits/FOct110033.imh.fits,imagenesfits/FOct110034.imh.fits,imagenesfits/FOct110035.imh.fits,imagenesfits/FOct110036.imh.fits,imagenesfits/FOct110037.imh.fits,imagenesfits/FOct110038.imh.fits,imagenesfits/FOct110039.imh.fits,imagenesfits/FOct110040.imh.fits,imagenesfits/FOct110041.imh.fits,imagenesfits/FOct110042.imh.fits,imagenesfits/FOct110043.imh.fits,imagenesfits/FOct110044.imh.fits,imagenesfits/FOct110045.imh.fits,imagenesfits/FOct110046.imh.fits,imagenesfits/FOct110047.imh.fits,imagenesfits/FOct110048.imh.fits,imagenesfits/FOct110049.imh.fits,imagenesfits/FOct110050.imh.fits,imagenesfits/FOct110051.imh.fits,imagenesfits/FOct110052.imh.fits,imagenesfits/FOct110053.imh.fits,imagenesfits/FOct110054.imh.fits,imagenesfits/FOct110055.imh.fits,imagenesfits/FOct110056.imh.fits,imagenesfits/FOct110057.imh.fits,imagenesfits/FOct110058.imh.fits,imagenesfits/FOct110059.imh.fits,imagenesfits/FOct110060.imh.fits,imagenesfits/FOct110061.imh.fits,imagenesfits/FOct110062.imh.fits,imagenesfits/FOct110063.imh.fits,imagenesfits/FOct110064.imh.fits,imagenesfits/FOct110065.imh.fits,imagenesfits/FOct110066.imh.fits,imagenesfits/FOct110067.imh.fits,imagenesfits/FOct110068.imh.fits,imagenesfits/FOct110069.imh.fits,imagenesfits/FOct110070.imh.fits,imagenesfits/FOct110071.imh.fits,imagenesfits/FOct110072.imh.fits,imagenesfits/FOct110073.imh.fits,imagenesfits/FOct110074.imh.fits,imagenesfits/FOct110075.imh.fits,imagenesfits/FOct110076.imh.fits,imagenesfits/FOct110077.imh.fits,imagenesfits/FOct110078.imh.fits,imagenesfits/FOct110079.imh.fits,imagenesfits/FOct110080.imh.fits,imagenesfits/FOct110081.imh.fits,imagenesfits/FOct110082.imh.fits,imagenesfits/FOct110083.imh.fits,imagenesfits/FOct110084.imh.fits,imagenesfits/FOct110085.imh.fits,imagenesfits/FOct110086.imh.fits,imagenesfits/FOct110087.imh.fits")
		iraf.colbias.setParam('output', "new/FOct110001.imh.fits,new/FOct110002.imh.fits,new/FOct110003.imh.fits,new/FOct110004.imh.fits,new/FOct110005.imh.fits,new/FOct110007.imh.fits,new/FOct110008.imh.fits,new/FOct110009.imh.fits,new/FOct110010.imh.fits,new/FOct110011.imh.fits,new/FOct110012.imh.fits,new/FOct110013.imh.fits,new/FOct110014.imh.fits,new/FOct110015.imh.fits,new/FOct110016.imh.fits,new/FOct110017.imh.fits,new/FOct110018.imh.fits,new/FOct110019.imh.fits,new/FOct110020.imh.fits,new/FOct110022.imh.fits,new/FOct110023.imh.fits,new/FOct110024.imh.fits,new/FOct110025.imh.fits,new/FOct110026.imh.fits,new/FOct110027.imh.fits,new/FOct110028.imh.fits,new/FOct110029.imh.fits,new/FOct110030.imh.fits,new/FOct110031.imh.fits,new/FOct110032.imh.fits,new/FOct110033.imh.fits,new/FOct110034.imh.fits,new/FOct110035.imh.fits,new/FOct110036.imh.fits,new/FOct110037.imh.fits,new/FOct110038.imh.fits,new/FOct110039.imh.fits,new/FOct110040.imh.fits,new/FOct110041.imh.fits,new/FOct110042.imh.fits,new/FOct110043.imh.fits,new/FOct110044.imh.fits,new/FOct110045.imh.fits,new/FOct110046.imh.fits,new/FOct110047.imh.fits,new/FOct110048.imh.fits,new/FOct110049.imh.fits,new/FOct110050.imh.fits,new/FOct110051.imh.fits,new/FOct110052.imh.fits,new/FOct110053.imh.fits,new/FOct110054.imh.fits,new/FOct110055.imh.fits,new/FOct110056.imh.fits,new/FOct110057.imh.fits,new/FOct110058.imh.fits,new/FOct110059.imh.fits,new/FOct110060.imh.fits,new/FOct110061.imh.fits,new/FOct110062.imh.fits,new/FOct110063.imh.fits,new/FOct110064.imh.fits,new/FOct110065.imh.fits,new/FOct110066.imh.fits,new/FOct110067.imh.fits,new/FOct110068.imh.fits,new/FOct110069.imh.fits,new/FOct110070.imh.fits,new/FOct110071.imh.fits,new/FOct110072.imh.fits,new/FOct110073.imh.fits,new/FOct110074.imh.fits,new/FOct110075.imh.fits,new/FOct110076.imh.fits,new/FOct110077.imh.fits,new/FOct110078.imh.fits,new/FOct110079.imh.fits,new/FOct110080.imh.fits,new/FOct110081.imh.fits,new/FOct110082.imh.fits,new/FOct110083.imh.fits,new/FOct110084.imh.fits,new/FOct110085.imh.fits,new/FOct110086.imh.fits,new/FOct110087.imh.fits")
		iraf.colbias()

trimImages()
