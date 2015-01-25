import commands,sys
from glob import glob
from configLocal import OUTPUTDIR
from math import ceil

objName = sys.argv[1]
nInRow = 3

status, output =  commands.getstatusoutput("find %s/ -name %sCHARTS -print" % (OUTPUTDIR, objName))
ntot = 0
cmd = ""
for chf in output.split('\n'):
	print chf
	lf = glob("%s/*fits.png" % chf)
	ntot+=len(lf)
	cmd+=" ".join(lf)
	cmd += " "
print("montage %s -tile %dx%d  MONTAGE%s.png" % (cmd, 3,ceil(ntot/3.0), objName))
import os	
os.system("montage %s -tile %dx%d -geometry 640x480+0+0 MONTAGE%s.png" % (cmd, 3,ceil(ntot/3.0),objName))

