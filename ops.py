# Copyright (C) 2012 Christian Dersch <chrisdersch@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
from pyraf import iraf

# Initialize IRAF with ccdred
iraf.noao.imred(Stdout=1)
iraf.noao.imred.ccdred(Stdout=1)


def trimPicture(image, output, trimsec):
  iraf.ccdproc.setParam('images', image)
  iraf.ccdproc.setParam('output', output)
  iraf.ccdproc.setParam('ccdtype', '')
  iraf.ccdproc.setParam('fixpix', 'no')
  iraf.ccdproc.setParam('overscan', 'no')
  iraf.ccdproc.setParam('trim', 'yes')
  iraf.ccdproc.setParam('zerocor', 'no')
  iraf.ccdproc.setParam('darkcor', 'no')
  iraf.ccdproc.setParam('flatcor', 'no')
  iraf.ccdproc.setParam('illumco', 'no')
  iraf.ccdproc.setParam('readcor', 'no')
  iraf.ccdproc.setParam('scancor', 'no')
  iraf.ccdproc.setParam('trimsec', trimsec)
  iraf.ccdproc()
  

def createMasterdark(imagelist, output):
  _file = open('input.tmp', 'w')
  for image in imagelist:
    _file.write(image+'\n')
  _file.close()
  iraf.darkcombine.setParam('input', '@input.tmp')
  iraf.darkcombine.setParam('output', output)
  iraf.darkcombine.setParam('ccdtype', '')
  iraf.darkcombine.setParam('process', 'no')
  iraf.darkcombine()
  os.system('rm input.tmp')
  
  
def darkCorrect(image, output, dark):
  iraf.ccdproc.setParam('images', image)
  iraf.ccdproc.setParam('output', output)
  iraf.ccdproc.setParam('ccdtype', '')
  iraf.ccdproc.setParam('fixpix', 'no')
  iraf.ccdproc.setParam('overscan', 'no')
  iraf.ccdproc.setParam('trim', 'no')
  iraf.ccdproc.setParam('zerocor', 'no')
  iraf.ccdproc.setParam('darkcor', 'yes')
  iraf.ccdproc.setParam('flatcor', 'no')
  iraf.ccdproc.setParam('illumco', 'no')
  iraf.ccdproc.setParam('readcor', 'no')
  iraf.ccdproc.setParam('scancor', 'no')
  iraf.ccdproc.setParam('dark', dark)
  iraf.ccdproc()

