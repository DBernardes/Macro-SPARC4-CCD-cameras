#!/usr/bin/env python
# coding: utf-8

# Fiz este codigo para confirmar se os valores de ruido calculados pela biblioteca estavam corretos.

import Read_Noise_Calculation_Bib as RNC
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm, lines
import numpy as np


def f(em_mode=1, em_gain=2, hss=1, preamp=1, binn=1):    
    RN = RNC.ReadNoiseCalc()    
    RN.write_operation_mode(em_mode, em_gain, hss, preamp, binn)
    #RN.get_operation_mode()
    RN.calc_read_noise()
    read_noise = float(RN.noise)
    
    return read_noise


def calc_vetor_read_noise(preamp, binning):
    em_gain = np.linspace(2,300,20)
    HSS = [1,10,20,30]
    len_HSS = len(HSS)
    len_gain = len(em_gain)
    read_noise, xs, ys = [], [], []

    for hss in HSS:
        for gain in em_gain:
            em_mode = [1, gain, hss, preamp, binning]      
            noise = f(em_mode)
            xs.append(hss)
            ys.append(gain)
            read_noise.append(noise)
    return xs, ys, read_noise




fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
xs, ys, read_noise = calc_vetor_read_noise(preamp=1, binning=1)
ax.plot_trisurf(xs, ys, read_noise, cmap='autumn',linewidth=1, antialiased=True)
xs, ys, read_noise = calc_vetor_read_noise(preamp=2, binning=1)
ax.plot_trisurf(xs, ys, read_noise, cmap='winter',linewidth=1, antialiased=True)
ax.set_alpha(0.3)
ax.set_xlabel(r'Horizontal Shift Speed (MHz)')
ax.set_ylabel(r'EM Gain')
ax.set_zlabel(r'Ruído de Leitura do CCD (e-)')
fake2Dline = lines.Line2D([0],[0], linestyle="none", c='r', marker = 'o')
fake2Dline2 = lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
ax.legend([fake2Dline, fake2Dline2], [r'Preamp 1, Binning 1', r'Preamp 2, Binning 1'], numpoints = 1)




ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.set_alpha(0.3)
xs, ys, read_noise = calc_vetor_read_noise(preamp=1, binning=2)
ax.plot_trisurf(xs, ys, read_noise, cmap='autumn',linewidth=1, antialiased=True)
xs, ys, read_noise = calc_vetor_read_noise(preamp=2, binning=2)
ax.plot_trisurf(xs, ys, read_noise, cmap='winter',linewidth=1, antialiased=True)
ax.set_xlabel(r'Horizontal Shift Speed (MHz)')
ax.set_ylabel(r'EM Gain')
ax.set_zlabel(r'Ruído de Leitura do CCD (e-)')
fake2Dline = lines.Line2D([0],[0], linestyle="none", c='r', marker = 'o')
fake2Dline2 = lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
ax.legend([fake2Dline, fake2Dline2], [r'Preamp 1, Binning 2', r'Preamp 2, Binning 2'], numpoints = 1)
plt.show()

