import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
x = np.array([1.059,1.052,1.049,1.067]) #RFILTER
y = np.array([14.5, 14.6, 13.8, 14.5])	#RFILTER
#x = np.array([1.059,1.052,1.049,1.067]) #RFILTER
#y = np.array([14.5, 14.6, 13.8, 14.5])	#RFILTER
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
