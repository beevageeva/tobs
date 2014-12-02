from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
print("X=")
print(X)
print("Y=")
print(Y)
print("Z=")
print(Z)
print("shapex")
print(X.shape)
print("shapey")
print(Y.shape)
print("shapez")
print(Z.shape)
cset = ax.contour(X, Y, Z, cmap=cm.coolwarm)
ax.clabel(cset, fontsize=9, inline=1)

plt.show()
