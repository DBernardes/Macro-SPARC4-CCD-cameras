"""
=============================================
Generate polygons to fill under 3D line graph
=============================================

Demonstrate how to create polygons which fill the space under a line
graph. In this example polygons are semi-transparent, creating a sort
of 'jagged stained glass' effect.
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import sys

import Read_Noise_Calculation_Bib as RNC
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def f(em_mode=1, em_gain=2, hss=1, preamp=1, binn=1):    
    RN = RNC.ReadNoiseCalc()    
    RN.write_operation_mode(em_mode, em_gain, hss, preamp, binn)
    #RN.get_operation_mode()
    RN.calc_read_noise()
    read_noise = float(RN.noise)
    
    return read_noise

em_gain = np.linspace(2,300,5)
HSS = [1,10,20,30]

len_HSS = len(HSS)
len_gain = len(em_gain)
xs=[]
ys=[]
read_noise = []

for hss in HSS:
    for gain in em_gain:
        em_mode = [1, gain, hss, 2, 2]      
        noise = f(em_mode)
        xs.append(hss)
        ys.append(gain)
        read_noise.append(noise)       





fig = plt.figure()
ax = fig.gca(projection='3d')


def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)


verts = []
for z in read_noise:    
    verts.append(list(zip(xs, ys)))

poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'), cc('y')])
poly.set_alpha(0.5)
ax.add_collection3d(poly, zs=read_noise, zdir='z')

ax.set_xlabel('X')
ax.set_xlim3d(0, 40)
ax.set_ylabel('Y')
ax.set_ylim3d(0, 300)
ax.set_zlabel('Z')
ax.set_zlim3d(0, 500)

plt.show()


