#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from Funcoes_Bib import splitPlusMinus




df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Ganho_EM\Preamp2\Propagado.xlsm') 
columns = pd.DataFrame(df)


gain = columns['EM Gain'][0:6]
noise = columns['Noise (ADU)'][0:6]
median = np.median(noise)
error = columns['Error (ADU)'][0:6]#np.median(abs(GAIN['noise'] - median))/0.67449
#print temp['value'], temp['noise'], temp['error']



# Constroi o modelo parabolico
x = np.linspace(0,50,100)
f1 = lambda x,a,b,c: a*x**2 + b*x +c

#constroi o modelo exponencial
f2 = lambda x,a,b: a**x + b

# Faz o ajuste para cada regime, dado o modelo
R1popt, R1pcov = curve_fit(f1, gain, noise)
R2popt, R2pcov = curve_fit(f2, gain, noise)

residuos1 = noise - f1(gain, R1popt[0],R1popt[1], R1popt[2])
residuos2 = noise - f2(gain, R2popt[0],R2popt[1])



# In[2]:


fontsize = 15
fig = plt.figure(figsize=(14, 4))
ax = fig.add_subplot(121)
ax.errorbar(gain, noise, error, marker='o', c='blue',linewidth=1.0)
ax.plot(x, f1(x,R1popt[0],R1popt[1], R1popt[2]), '--', c='red')
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(1.3, 3.5)
#plt.xlim(-5, 305)

string1 = r'$\mathtt{f(x) = %.6f x^2 + %.4f x + %.3f}$'%(R1popt[0],R1popt[1],R1popt[2])
string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R1pcov[0][0]) + '\n      ' + r'$\mathtt{%.2e,}$'%(R1pcov[1][1]) +'\n      ' + r'$\mathtt{%.2e }$' %(R1pcov[2][2])
ax.text(0.1, 0.9, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.1, 0.7, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

ax = fig.add_subplot(122)
ax.errorbar(gain, residuos1, error, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad dos \quad res \acute{\i} duos }$', size=fontsize)
plt.show()


# In[3]:


fontsize = 15
fig = plt.figure(figsize=(14, 4))
ax = fig.add_subplot(121)
ax.errorbar(gain, noise, error, marker='o', c='blue',linewidth=1.0)
ax.plot(x, f2(x,R2popt[0],R2popt[1]), '--', c='red')
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(1.3, 3.5)
#plt.xlim(-5, 305)

string1 = r'$\mathtt{f(x) = %.3f^x + %.3f}$'%(R2popt[0],R2popt[1])
string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R2pcov[0][0]) + '\n      ' + r'$\mathtt{%.2e,}$'%(R2pcov[1][1])
ax.text(0.1, 0.9, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.1, 0.7, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

ax = fig.add_subplot(122)
ax.errorbar(gain, residuos2, error, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad dos \quad res \acute{\i} duos }$', size=fontsize)

plt.show()

