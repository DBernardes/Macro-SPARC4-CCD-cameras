#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from Funcoes_Bib import splitPlusMinus

#-------------------------------------------------------PA1B1--------------------------------------------------------------------------

dir_path = r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Planilhas_Caracterizacoes\Ganho_EM\Preamp1_B1'
name1MHz =  '\HSS1MHz\Propagado.xlsm'
name10MHz = '\HSS10MHz\Propagado.xlsm'
name20MHz = '\HSS20MHz\Propagado.xlsm'
name30MHz = '\HSS30MHz\Propagado.xlsm'

df = pd.read_excel (dir_path + name1MHz) 
columns = pd.DataFrame(df)
HSS1PA1CCDgain = 15.9
gainPA1B1HSS1 = columns['EM Gain'][0:11]
noisePA1B1HSS1 = columns['Noise (ADU)'][0:11]*HSS1PA1CCDgain
errorPA1B1HSS1 = columns['Error (ADU)'][0:11]*HSS1PA1CCDgain

df = pd.read_excel (dir_path + name10MHz) 
columns = pd.DataFrame(df)
HSS10PA1CCDgain = 16.0
gainPA1B1HSS10 = columns['EM Gain'][0:11]
noisePA1B1HSS10 = columns['Noise (ADU)'][0:11]*HSS10PA1CCDgain
errorPA1B1HSS10 = columns['Error (ADU)'][0:11]*HSS10PA1CCDgain

df = pd.read_excel (dir_path + name20MHz) 
columns = pd.DataFrame(df)
HSS20PA1CCDgain = 16.4
gainPA1B1HSS20 = columns['EM Gain'][0:11]
noisePA1B1HSS20 = columns['Noise (ADU)'][0:11]*HSS20PA1CCDgain
errorPA1B1HSS20 = columns['Error (ADU)'][0:11]*HSS20PA1CCDgain

df = pd.read_excel (dir_path + name30MHz) 
columns = pd.DataFrame(df)
HSS30PA1CCDgain = 17.2
gainPA1B1HSS30 = columns['EM Gain'][0:11]
noisePA1B1HSS30 = columns['Noise (ADU)'][0:11]*HSS30PA1CCDgain
errorPA1B1HSS30 = columns['Error (ADU)'][0:11]*HSS30PA1CCDgain

fontsize = 12
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(221)
ax.errorbar(gainPA1B1HSS1, noisePA1B1HSS1, errorPA1B1HSS1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{1 \; MHz}$')
ax.errorbar(gainPA1B1HSS10, noisePA1B1HSS10, errorPA1B1HSS10, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{10 \; MHz}$')
ax.errorbar(gainPA1B1HSS20, noisePA1B1HSS20, errorPA1B1HSS20, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{20 \; MHz}$')
ax.errorbar(gainPA1B1HSS30, noisePA1B1HSS30, errorPA1B1HSS30, marker='o', c='black',linewidth=1.0, label=r'$\mathtt{30 \; MHz}$')
#plt.xlabel(r'$\mathtt{EM \quad gain }$', size=fontsize)
plt.ylabel(r'$\mathtt{Noise (e-)}$', size=fontsize)
plt.rc('xtick', labelsize=fontsize) 
plt.rc('ytick', labelsize=fontsize)
#plt.title(r'$\mathtt{Preamp \quad 1 \quad and \quad Binning \quad 1}$', size=fontsize)
#plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 400)
plt.legend(bbox_to_anchor=(0, 0, 1, 0.85), ncol=2, prop={'size': fontsize})



#-------------------------------------------------------PA1B2--------------------------------------------------------------------------


dir_path = r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Planilhas_Caracterizacoes\Ganho_EM\Preamp1_B2'

df = pd.read_excel (dir_path + name1MHz) 
columns = pd.DataFrame(df)
HSS1PA1CCDgain = 15.9
gainPA1B2HSS1 = columns['EM Gain'][0:11]
noisePA1B2HSS1 = columns['Noise (ADU)'][0:11]*HSS1PA1CCDgain
errorPA1B2HSS1 = columns['Error (ADU)'][0:11]*HSS1PA1CCDgain

df = pd.read_excel (dir_path + name10MHz) 
columns = pd.DataFrame(df)
HSS10PA1CCDgain = 16.0
gainPA1B2HSS10 = columns['EM Gain'][0:11]
noisePA1B2HSS10 = columns['Noise (ADU)'][0:11]*HSS10PA1CCDgain
errorPA1B2HSS10 = columns['Error (ADU)'][0:11]*HSS10PA1CCDgain

df = pd.read_excel (dir_path + name20MHz) 
columns = pd.DataFrame(df)
HSS20PA1CCDgain = 16.4
gainPA1B2HSS20 = columns['EM Gain'][0:11]
noisePA1B2HSS20 = columns['Noise (ADU)'][0:11]*HSS20PA1CCDgain
errorPA1B2HSS20 = columns['Error (ADU)'][0:11]*HSS20PA1CCDgain

df = pd.read_excel (dir_path + name30MHz) 
columns = pd.DataFrame(df)
HSS30PA1CCDgain = 17.2
gainPA1B2HSS30 = columns['EM Gain'][0:11]
noisePA1B2HSS30 = columns['Noise (ADU)'][0:11]*HSS30PA1CCDgain
errorPA1B2HSS30 = columns['Error (ADU)'][0:11]*HSS30PA1CCDgain


ax = fig.add_subplot(222)
ax.errorbar(gainPA1B2HSS1, noisePA1B2HSS1, errorPA1B2HSS1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{1 \; MHz}$')
ax.errorbar(gainPA1B2HSS10, noisePA1B2HSS10, errorPA1B2HSS10, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{10 \; MHz}$')
ax.errorbar(gainPA1B2HSS20, noisePA1B2HSS20, errorPA1B2HSS20, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{20 \; MHz}$')
ax.errorbar(gainPA1B2HSS30, noisePA1B2HSS30, errorPA1B2HSS30, marker='o', c='black',linewidth=1.0, label=r'$\mathtt{30 \; MHz}$')
#plt.xlabel(r'$\mathtt{EM \quad gain }$', size=fontsize)
#plt.ylabel(r'$\mathtt{Noise (e-)}$', size=fontsize)
plt.rc('xtick', labelsize=fontsize) 
plt.rc('ytick', labelsize=fontsize)
#plt.title(r'$\mathtt{Preamp \quad 1 \quad and \quad Binning \quad 2}$', size=fontsize)
#plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 400)
plt.legend(bbox_to_anchor=(0, 0, 1, 0.85), ncol=2, prop={'size': fontsize})



#-------------------------------------------------------PA2B1--------------------------------------------------------------------------


dir_path = r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Planilhas_Caracterizacoes\Ganho_EM\Preamp2_B1'

df = pd.read_excel (dir_path + name1MHz) 
columns = pd.DataFrame(df)
HSS1PA2CCDgain = 3.88
gainPA2B1HSS1 = columns['EM Gain'][0:11]
noisePA2B1HSS1 = columns['Noise (ADU)'][0:11]*HSS1PA2CCDgain
errorPA2B1HSS1 = columns['Error (ADU)'][0:11]*HSS1PA2CCDgain

df = pd.read_excel (dir_path + name10MHz) 
columns = pd.DataFrame(df)
HSS10PA2CCDgain = 3.96
gainPA2B1HSS10 = columns['EM Gain'][0:11]
noisePA2B1HSS10 = columns['Noise (ADU)'][0:11]*HSS10PA2CCDgain
errorPA2B1HSS10 = columns['Error (ADU)'][0:11]*HSS10PA2CCDgain

df = pd.read_excel (dir_path + name20MHz) 
columns = pd.DataFrame(df)
HSS20PA2CCDgain = 4.39
gainPA2B1HSS20 = columns['EM Gain'][0:11]
noisePA2B1HSS20 = columns['Noise (ADU)'][0:11]*HSS20PA2CCDgain
errorPA2B1HSS20 = columns['Error (ADU)'][0:11]*HSS20PA2CCDgain

df = pd.read_excel (dir_path + name30MHz) 
columns = pd.DataFrame(df)
HSS30PA2CCDgain = 5.27
gainPA2B1HSS30 = columns['EM Gain'][0:11]
noisePA2B1HSS30 = columns['Noise (ADU)'][0:11]*HSS30PA2CCDgain
errorPA2B1HSS30 = columns['Error (ADU)'][0:11]*HSS30PA2CCDgain

ax = fig.add_subplot(223)
ax.errorbar(gainPA2B1HSS1, noisePA2B1HSS1, errorPA2B1HSS1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{1 \; MHz}$')
ax.errorbar(gainPA2B1HSS10, noisePA2B1HSS10, errorPA2B1HSS10, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{10 \; MHz}$')
ax.errorbar(gainPA2B1HSS20, noisePA2B1HSS20, errorPA2B1HSS20, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{20 \; MHz}$')
ax.errorbar(gainPA2B1HSS30, noisePA2B1HSS30, errorPA2B1HSS30, marker='o', c='black',linewidth=1.0, label=r'$\mathtt{30 \; MHz}$')
plt.xlabel(r'$\mathtt{EM \quad gain}$', size=fontsize)
plt.ylabel(r'$\mathtt{Noise (e-)}$', size=fontsize)
#plt.title(r'$\mathtt{Preamp \quad 2 \quad and \quad Binning \quad 1}$', size=fontsize)
plt.rc('xtick', labelsize=fontsize) 
plt.rc('ytick', labelsize=fontsize)
#plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 400)
plt.legend(bbox_to_anchor=(0, 0, 1, 0.85), ncol=2, prop={'size': fontsize})


#-------------------------------------------------------PA2B2--------------------------------------------------------------------------


dir_path = r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Planilhas_Caracterizacoes\Ganho_EM\Preamp2_B2'

df = pd.read_excel (dir_path + name1MHz) 
columns = pd.DataFrame(df)
HSS1PA2CCDgain = 3.88
gainPA2B2HSS1 = columns['EM Gain'][0:11]
noisePA2B2HSS1 = columns['Noise (ADU)'][0:11]*HSS1PA2CCDgain
errorPA2B2HSS1 = columns['Error (ADU)'][0:11]*HSS1PA2CCDgain

df = pd.read_excel (dir_path + name10MHz) 
columns = pd.DataFrame(df)
HSS10PA2CCDgain = 3.96
gainPA2B2HSS10 = columns['EM Gain'][0:11]
noisePA2B2HSS10 = columns['Noise (ADU)'][0:11]*HSS10PA2CCDgain
errorPA2B2HSS10 = columns['Error (ADU)'][0:11]*HSS10PA2CCDgain

df = pd.read_excel (dir_path + name20MHz) 
columns = pd.DataFrame(df)
HSS20PA2CCDgain = 4.39
gainPA2B2HSS20 = columns['EM Gain'][0:11]
noisePA2B2HSS20 = columns['Noise (ADU)'][0:11]*HSS20PA2CCDgain
errorPA2B2HSS20 = columns['Error (ADU)'][0:11]*HSS20PA2CCDgain

df = pd.read_excel (dir_path + name30MHz) 
columns = pd.DataFrame(df)
HSS30PA2CCDgain = 5.27
gainPA2B2HSS30 = columns['EM Gain'][0:11]
noisePA2B2HSS30 = columns['Noise (ADU)'][0:11]*HSS30PA2CCDgain
errorPA2B2HSS30 = columns['Error (ADU)'][0:11]*HSS30PA2CCDgain

ax = fig.add_subplot(224)
ax.errorbar(gainPA2B2HSS1, noisePA2B2HSS1, errorPA2B2HSS1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{1 \; MHz}$')
ax.errorbar(gainPA2B2HSS10, noisePA2B2HSS10, errorPA2B2HSS10, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{10 \; MHz}$')
ax.errorbar(gainPA2B2HSS20, noisePA2B2HSS20, errorPA2B2HSS20, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{20 \; MHz}$')
ax.errorbar(gainPA2B2HSS30, noisePA2B2HSS30, errorPA2B2HSS30, marker='o', c='black',linewidth=1.0, label=r'$\mathtt{30 \; MHz}$')
plt.xlabel(r'$\mathtt{EM \quad gain}$', size=fontsize)
#plt.ylabel(r'$\mathtt{Noise (e-)}$', size=fontsize)
#plt.title(r'$\mathtt{Preamp \quad 2 \quad and \quad Binning \quad 2}$', size=fontsize)
plt.rc('xtick', labelsize=fontsize) 
plt.rc('ytick', labelsize=fontsize)
#plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 400)
plt.legend(bbox_to_anchor=(0, 0, 1, 0.85), ncol=2, prop={'size': fontsize})
plt.show()



##fontsize = 14
##fig = plt.figure(figsize=(6, 6))
##ax = fig.add_subplot(111)
##ax.errorbar(gainPA1B1HSS1, noisePA1B1HSS1, errorPA1B1HSS1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{PA1B1HSS1}$')
##ax.errorbar(gainPA1B1HSS10, noisePA1B1HSS10, errorPA1B1HSS10, marker='^', c='blue',linewidth=1.0, label=r'$\mathtt{PA1B1HSS10}$')
##ax.errorbar(gainPA1B1HSS20, noisePA1B1HSS20, errorPA1B1HSS20, marker='d', c='blue',linewidth=1.0, label=r'$\mathtt{PA1B1HSS20}$')
##ax.errorbar(gainPA1B1HSS30, noisePA1B1HSS30, errorPA1B1HSS30, marker='s', c='blue',linewidth=1.0, label=r'$\mathtt{PA1B1HSS30}$')
##
##ax.errorbar(gainPA2B1HSS1, noisePA2B1HSS1, errorPA2B1HSS1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{PA2B1HSS1}$')
##ax.errorbar(gainPA2B1HSS10, noisePA2B1HSS10, errorPA2B1HSS10, marker='^', c='green',linewidth=1.0, label=r'$\mathtt{PA2B1HSS10}$')
##ax.errorbar(gainPA2B1HSS20, noisePA2B1HSS20, errorPA2B1HSS20, marker='d', c='green',linewidth=1.0, label=r'$\mathtt{PA2B1HSS20}$')
##ax.errorbar(gainPA2B1HSS30, noisePA2B1HSS30, errorPA2B1HSS30, marker='s', c='green',linewidth=1.0, label=r'$\mathtt{PA2B1HSS30}$')
##
##ax.errorbar(gainPA1B2HSS1, noisePA1B2HSS1, errorPA1B2HSS1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{PA1B2HSS1}$')
##ax.errorbar(gainPA1B2HSS10, noisePA1B2HSS10, errorPA1B2HSS10, marker='^', c='red',linewidth=1.0, label=r'$\mathtt{PA1B2HSS10}$')
##ax.errorbar(gainPA1B2HSS20, noisePA1B2HSS20, errorPA1B2HSS20, marker='d', c='red',linewidth=1.0, label=r'$\mathtt{PA1B2HSS20}$')
##ax.errorbar(gainPA1B2HSS30, noisePA1B2HSS30, errorPA1B2HSS30, marker='s', c='red',linewidth=1.0, label=r'$\mathtt{PA1B2HSS30}$')
##
##ax.errorbar(gainPA2B2HSS1, noisePA2B2HSS1, errorPA2B2HSS1, marker='o', c='black',linewidth=1.0, label=r'$\mathtt{PA2B2HSS1}$')
##ax.errorbar(gainPA2B2HSS10, noisePA2B2HSS10, errorPA2B2HSS10, marker='^', c='black',linewidth=1.0, label=r'$\mathtt{PA2B2HSS10}$')
##ax.errorbar(gainPA2B2HSS20, noisePA2B2HSS20, errorPA2B2HSS20, marker='d', c='black',linewidth=1.0, label=r'$\mathtt{PA2B2HSS20}$')
##ax.errorbar(gainPA2B2HSS30, noisePA2B2HSS30, errorPA2B2HSS30, marker='s', c='black',linewidth=1.0, label=r'$\mathtt{PA2B2HSS30}$')
##
##plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
##plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
##plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
###plt.ylim(15, 23)
##plt.xlim(-5, 450)
##plt.legend(bbox_to_anchor=(0, 0, 1, 0.95))#, ncol=2)
##plt.show()

