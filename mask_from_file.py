from pyraf import iraf
import sys, shutil

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.ccdred(Stdout=1)



def makeMask(resFile):
	shutil.copy(resFile, resFile+".orig")
	iraf.ccdmask.setParam("image", resFile)
	maskFile = resFile + ".mask"
	iraf.ccdmask.setParam("mask", maskFile)
	iraf.ccdmask(Stdout=1, mode="h")

	iraf.fixpix.setParam("images", resFile )
	iraf.fixpix.setParam("masks", maskFile+ ".pl")
	iraf.fixpix(Stdout=1, mode="h")



makeMask(sys.argv[1])
