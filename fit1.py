import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
#x = np.array([1.059, 1.052, 1.049, 1.067]) #RFILTER
x = np.array([14.2, 14.2, 14.3]) #VFILTER
#x = np.array([15.9, 15.9,15.9]) #UFILTER
#y = np.array([13.7, 13.7, 13.2, 13.6])	#RFILTER
y = np.array([1.069, 1.061, 1.054])	#VFILTER
#y = np.array([1.064, 1.056, 1.072])	#UFILTER
z = np.polyfit(x, y, 1)
print z
print("%4.3f x + %4.3f" % (z[0], z[1]))
tyFunc = np.poly1d(z)
ty = tyFunc(x)
plt.plot(x,y,'ro')
plt.plot(x,ty,'b-')
print("m0 = %e" % tyFunc(0))
plt.draw()
plt.show()
