import os,sys
import pyfits,numpy
import re
from pyraf import iraf

iraf.noao.imred(Stdout=1)


import matplotlib.pyplot as plt

def displaySt(fitsfile , delta, plotImages=False):
	im = pyfits.getdata(fitsfile)
	print("shape of im")
	print(im.shape)	
	res = iraf.imstat(fitsfile, Stdout=1)	
	#print("imstat:\n")
	#print(res)	
	# IMAGENAME NPIX      MEAN    STDDEV       MIN       MAX
	resArray = re.split("\s+", res[1].strip())
	print("imagename = %s" % resArray[0])
	print("Npix = %s" % resArray[1])
	print("Mean = %s" % resArray[2])
	print("Stddev = %s" % resArray[3])
	print("Min = %s" % resArray[4])
	maxValue = float(resArray[5])
	print("Max = %4.1f" % maxValue)
	print("indices where data > maxValue * %1.2f" % delta)
	ind = numpy.where(im > delta * maxValue)	

	print("Number of points = %d" % len(ind[0]) )

	obj = []
	for i in range(0, len(ind[0])):
		row = ind[0][i]	
		col = ind[1][i]
		#for o in obj:
		#print(numpy.logical_or(ind[0]==row-1, numpy.logical_or(ind[0]==row, ind[0]==row+1)))
		#print(numpy.logical_or(ind[1]==col-1, numpy.logical_or(ind[1]==col, ind[1]==col+1)))
		#no need to look backwards
		#andCond = numpy.logical_and(numpy.logical_or(ind[0]==row-1, numpy.logical_or(ind[0]==row, ind[0]==row+1)),numpy.logical_or(ind[1]==col-1, numpy.logical_or(ind[1]==col, ind[1]==col+1)) )
		andCond = numpy.logical_and(numpy.logical_or(ind[0]==row, ind[0]==row+1),numpy.logical_or(ind[1]==col, ind[1]==col+1))
		ks = -1
		for k in range(0, len(obj)):
			for j in range(0, len(ind[0][andCond])):
				for n in range(0, len( obj[k]['i'])):
					if(ind[0][andCond][j] == obj[k]['i'][n] and  ind[1][andCond][j] == obj[k]['j'][n]):
						ks = k
						break
		if(ks>-1):
			for j in range(0, len(ind[0][andCond])):
				exists = False
				for n in range(0, len( obj[k]['i'])):
					if(ind[0][andCond][j] == obj[k]['i'][n] and  ind[1][andCond][j] == obj[k]['j'][n]):
						exists = True
				if(not exists):	
					obj[ks]['i'].append(ind[0][andCond][j])
					obj[ks]['j'].append(ind[1][andCond][j])
		else:
			obj.append({'i' : ind[0][andCond].tolist(), 'j':  ind[1][andCond].tolist() })		
		#print(ind[0][andCond])
		#print(ind[1][andCond])
		
	print("OBJ")
	print(obj)
 
	print("len(obj) = %d" % len(obj))


	#print("rows")
	#print(numpy.unique(ind[0]))
	#print("cols")
	#print(numpy.unique(ind[1]))
	

	#numpy.set_printoptions(threshold='nan')
	#print("array")
	#print(numpy.dstack((ind[0],ind[1])))
		
	#bigv = numpy.zeros((1024, 1024))
	#bigv[im > 0.99 * maxValue] = 1

	bigv = numpy.zeros((1024, 1024))
	rMark = 5
	for o in obj:
		mi = o['i'][int(len(o['i'])/2)]
		mj = o['j'][int(len(o['j'])/2)]
		print("mi=%d,mj=%d,i:%s,j:%s" % (mi,mj, ",".join(str(o['i'])), ",".join(str(o['j'])) ))
		bigv[mi-rMark:mi+rMark, mj-rMark:mj+rMark] = 1

	if(plotImages):
		fig = plt.figure(1)
		ax1= fig.add_subplot(1, 3, 1)
		ax2= fig.add_subplot(1, 3, 2)
		ax3= fig.add_subplot(1, 3, 3)
		ax1.imshow(bigv, cmap='gray',origin='lower')	
		ax2.imshow(im, cmap='gray',origin='lower')	
		ax3.imshow(bigv, cmap='gray',origin='lower')
		ax3.imshow(im, cmap='gray',origin='lower', alpha=0.5)
		plt.draw()
		plt.show(block=True)


delta = float(sys.argv[2])
displaySt(sys.argv[1], delta)

 
