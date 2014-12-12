import numpy as np
import sys


x,y,z = np.loadtxt(sys.argv[1], usecols=[2,3,4], unpack=True)
print(x)
print("sky mean is %4.2f" % np.mean(x) )
print(y)
print("sigma mean is %4.2f" % np.mean(y) )
print(z)
print("FWHMPSF mean is %4.2f" % np.mean(z) )
