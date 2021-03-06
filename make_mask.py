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

iraf.mskexpr.setParam("expr", "@/home/bpb/asign/tobs/pyraf/mask1.dat")
#iraf.mskexpr.setParam("expr", "@/home/bpb/asign/tobs/pyraf/expr.dat")
iraf.mskexpr.setParam("refimages", "")
iraf.mskexpr.setParam("refmasks", "")
iraf.mskexpr.setParam("dims", "1024,1024")
iraf.mskexpr.setParam("masks", "/home/bpb/asign/tobs/pyraf/mask1.mask.pl")
#iraf.mskexpr.setParam("masks", "/home/bpb/asign/tobs/pyraf/expr.mask.pl")
iraf.mskexpr()
