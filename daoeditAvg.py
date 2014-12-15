import numpy as np
import sys


#x,y,z = np.loadtxt(sys.argv[1], usecols=[2,3,4], unpack=True)
#no sky mean
y,z = np.loadtxt(sys.argv[1], usecols=[3,4], unpack=True)
#no sky mean
#print(x)
#print("sky mean is %4.2f" % np.mean(x) )
#print(y)
print("sky sigma mean is %4.2f" % np.mean(y) )
#print(z)
print("FWHMPSF mean is %4.2f" % np.mean(z) )
