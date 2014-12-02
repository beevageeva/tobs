from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#X, Y, Z = axes3d.get_test_data(0.05)

##start meshgrid
#a, b = 1, 1
#n = 7
#r = 3
#
#z = np.ones(n)
#y,x = np.ogrid[-a:n-a, -b:n-b]
#mask = x*x + y*y <= r*r
#
#array = np.ones((n, n))
#array[mask] = 255
#
#X, Y , Z = np.meshgrid(array[mask][0], array[mask][1], z)
#print("X=")
#print(X)
#print("Y=")
#print(Y)
#print("Z=")
#print(Z)
#print("shapex")
#print(X.shape)
#print("shapey")
#print(Y.shape)
#print("shapez")
#print(Z.shape)
##end meshgrid
##plot contour
#cset = ax.contour(X, Y, Z, cmap=cm.coolwarm)
#ax.clabel(cset, fontsize=9, inline=1)


z = np.ones(1000)
from math import pi
alpha = np.linspace(0, 2*pi , 1000)

x = np.sin(alpha)
y = np.cos(alpha)



ax.plot(x, y, z, '-b')



plt.show()
