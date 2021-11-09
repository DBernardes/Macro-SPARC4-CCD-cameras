#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit
from Funcoes_Bib import splitPlusMinus

df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Ganho_EM\HSS30MHz\EMPropagado.xlsm') 
columns = pd.DataFrame(df)

gain = columns['EM Gain'][0:11]
noise = columns['Noise (ADU)'][0:11]
median = np.median(noise)
error = columns['Error (ADU)'][0:11]#np.median(abs(GAIN['noise'] - median))/0.67449
#print temp['value'], temp['noise'], temp['error']


# Constroi o modelo parabolico
x = np.linspace(1,300,100)
f1 = lambda x,a,b,c,d,e: a*x**4 + b*x**3 +c*x**2 + d*x + e
#constroi o modelo exponencial
f2 = lambda x,a,b: x**(1/a) + b

# Faz o ajuste para cada regime, dado o modelo
R1popt, R1pcov = curve_fit(f1, gain, noise)
R2popt, R2pcov = curve_fit(f2, gain, noise)

residuos1 = noise - f1(gain, R1popt[0],R1popt[1], R1popt[2], R1popt[3],R1popt[4])
residuos2 = noise - f2(gain, R2popt[0],R2popt[1])



# In[2]:


fontsize = 14
fig = plt.figure(figsize=(14, 4))
ax = fig.add_subplot(121)
ax.errorbar(gain, noise, error, marker='o', c='blue',linewidth=1.0)
ax.plot(x, f1(x,R1popt[0],R1popt[1], R1popt[2], R1popt[3], R1popt[4]), '--', c='red')
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad fun \c c \tilde{a} o \quad do \quad Ganho \quad EM}$', size=fontsize)
#plt.ylim(15, 23)
#plt.xlim(-5, 305)

string1 = r'$\mathtt{f(x) = %.2e x^2 + %.2e x + %.2e}$'%(R1popt[0],R1popt[1],R1popt[2])
string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R1pcov[0][0])  + r'$\mathtt{%.2e,}$'%(R1pcov[1][1]) + r'$\mathtt{%.2e }$' %(R1pcov[2][2])
ax.text(0.06, 0.3, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.06, 0.1, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

ax = fig.add_subplot(122)
ax.errorbar(gain, residuos1, error, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad dos \quad res \acute{\i} duos }$', size=fontsize)
plt.show()


# In[4]:


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

string1 = r'$\mathtt{f(x) = x^{1/%.2f} + %.2f}$'%(R2popt[0],R2popt[1])
string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R2pcov[0][0]) + r'$\mathtt{%.2e}$'%(R2pcov[1][1])
ax.text(0.4, 0.3, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.4, 0.1, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

ax = fig.add_subplot(122)
ax.errorbar(gain, residuos2, error, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Ganho \quad EM}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad dos \quad res \acute{\i} duos }$', size=fontsize)

plt.show()

