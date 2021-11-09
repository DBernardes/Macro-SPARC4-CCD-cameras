#!/usr/bin/env python
# coding: utf-8

# Fiz este codigo para confirmar se os valores de ruido calculados pela biblioteca estavam corretos.

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

em_gain = np.linspace(2,300,20)
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
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs, ys, read_noise, c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

