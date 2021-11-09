#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit
from Funcoes_Bib import splitPlusMinus

df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Ganho_EM\HSS10MHz\Propagado.xlsm') 
columns = pd.DataFrame(df)

gainR1 = columns['EM Gain'][1:11]
noiseR1 = columns['Noise (ADU)'][1:11]
medianR1 = np.median(noiseR1)
errorR1 = columns['Error (ADU)'][1:11]#np.median(abs(GAIN['noise'] - median))/0.67449
#print temp['value'], temp['noise'], temp['error']

# Constroi o modelo de uma reta
x1 = np.linspace(10,300,100)
f1 = lambda x,a,b,: a*x + b
# Faz o ajuste para cada regime, dado o modelo
R1popt, R1pcov = curve_fit(f1, gainR1, noiseR1)
residuos1 = noiseR1 - f1(gainR1, R1popt[0],R1popt[1])




gainR2 = columns['EM Gain'][0:2]
noiseR2 = columns['Noise (ADU)'][0:2]
medianR2 = np.median(noiseR2)
errorR2 = columns['Error (ADU)'][0:2]

# Constroi o modelo de uma reta
x2 = np.linspace(2,10,50)
# Faz o ajuste para cada regime, dado o modelo
R2popt, R2pcov = curve_fit(f1, gainR2, noiseR2)
residuos2 = noiseR2 - f1(gainR2, R2popt[0],R2popt[1])




# In[26]:


fontsize = 14
fig = plt.figure(figsize=(14, 4))
ax = fig.add_subplot(121)
ax.errorbar(gainR1, noiseR1, errorR1, marker='o', c='blue',linewidth=1.0)
ax.errorbar(gainR2, noiseR2, errorR2, marker='o', c='blue',linewidth=1.0)
ax.plot(x1, f1(x1,R1popt[0],R1popt[1]), '--', c='red')
ax.plot(x2, f1(x2,R2popt[0],R2popt[1]), '--', c='red')

plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 305)

string1 = r'$\mathtt{f(x) = %.3f x + %.2f, \quad x < 10}$'%(R2popt[0],R2popt[1])
string2 = r'$\mathtt{%.4f x + %.2f, \quad x \geq 10}$'%(R1popt[0],R1popt[1])
#string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R1pcov[0][0])  + r'$\mathtt{%.2e,}$'%(R1pcov[1][1])

ax.text(0.35, 0.3, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.475, 0.1, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

ax = fig.add_subplot(122)
ax.errorbar(gainR1,residuos1,errorR1, marker='o', c='blue',linewidth=1.0)
ax.errorbar(gainR2[0], residuos2[0], errorR2[0], marker='o', c='blue',linewidth=1.0)

plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad dos \quad res \acute{\i} duos }$', size=fontsize)
plt.show()

