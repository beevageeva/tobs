import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as pyl
from matplotlib.contour import QuadContourSet
from matplotlib.widgets import Slider

#Define display parameters
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
delta = 0.025

#Define model parameters
alpha = .5
beta = .5
x_bar, a, b, c = 2, 0, 1, .1
v = np.arange(0, 10, delta)
w = np.arange(0, 10, delta)

#Calculate grid values
V, W = np.meshgrid(v,w)
Z = (V**(beta))*(W**(1-beta))
X = x_bar + a + b*Z
U = alpha*np.log(V) + (1-alpha)*np.log(X) - c*(W+V)

# Plot
fig = pyl.figure()

ax = fig.add_subplot(221)
CS = QuadContourSet(pyl.gca(), V, W, U, 200)
pyl.clabel(CS, inline=1, fontsize=10)
pyl.title('Simplest default with labels')

pyl.plot()
pyl.show(block=True)
