#!/usr/bin/env python
# coding: utf-8

# # Código para o gráfico do estudo do ruído

# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def splitPlusMinus(x, index=0):
    N = len(x)
    vector = np.asarray(np.zeros(N))
    error = np.asarray(np.zeros(N))
    for i in range(index, N+index):
        value = x[i].split(u'\xb1')
        vector[i-index] = (float(value[0]))
        error[i-index] = (float(value[1]))
        #print float(x[i].split(u'\xb1')[0])
    return vector, error


df = pd.read_excel (r'C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Estudo_do_ruido.xlsx') 
columns = pd.DataFrame(df)

binValue =  columns['Value'][0:4]
binNoise =  columns['Noise'][0:4]
tempValue = columns['Value'][8:13]
tempNoise = columns['Noise'][8:13]

binNoise, binError  = splitPlusMinus(binNoise)
tempNoise, tempError  = splitPlusMinus(tempNoise, 8)


# Constroi o modelo parabolico
x = np.linspace(1,8,100)
f1 = lambda x,a,b: a*x + b

# Faz o ajuste para cada regime, dado o modelo
R1popt, R1pcov = curve_fit(f1, binValue, binNoise)






# In[ ]:


fontsize = 15
plt.errorbar(tempValue, tempNoise,  tempError, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Temperatura (^oC)}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad func\c \tilde{a} o \quad da \quad temperatura}$', size=fontsize)
plt.ylim(1.5, 2.3)
plt.xlim(-81, -59)
plt.show()


# In[21]:


fontsize = 15

fontsize = 15
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.errorbar(binValue, binNoise,  binError, marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Binning}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad func\c \tilde{a} o \quad do \quad binning}$', size=fontsize)
#plt.ylim(1.5, 2.3)
#plt.xlim(-81, -59)

ax.plot(x, f1(x,R1popt[0],R1popt[1]), '--', c='red')
string1 = r'$\mathtt{f(x) = %.3f x + %.3f}$'%(R1popt[0],R1popt[1])
string2 = r'$\mathtt{\sigma^2 = %.2e,}$'%(R1pcov[0][0]) + '\n      ' + r'$\mathtt{%.2e}$'%(R1pcov[1][1]) 
ax.text(0.1, 0.9, string1, ha='left',va='center', transform=ax.transAxes, size=fontsize)
ax.text(0.1, 0.7, string2, ha='left',va='center', transform=ax.transAxes, size=fontsize)

plt.show()

