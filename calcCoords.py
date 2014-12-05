import os, shutil, re
from pyraf import iraf
from glob import glob
import numpy as np
import ds9

# Initialize IRAF with ccdred
iraf.noao.digiphot(Stdout=1)

from configLocal import IMGDIR, OUTPUTDIR, FILTERS

#d = ds9.ds9()


refImage =os.path.join(OUTPUTDIR, "object","V","Nov30098.fits")

#iraf.display(refImage,1) 
imx=iraf.imexam(refImage, frame = 1, Stdout=1, mode="h")

print("imx")
print(imx)

 









