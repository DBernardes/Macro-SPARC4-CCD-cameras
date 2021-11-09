#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Funcoes_Bib as FB
from scipy.optimize import curve_fit
from math import sqrt


# In[8]:


# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X1024_B1_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP1024B1 = columns['TEXP (s)'][0:21]
FREQ1024B1 = columns['FREQ (fps)'][0:21]

# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X512_B1_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP512B1 = columns['TEXP (s)'][0:26]
FREQ512B1 = columns['FREQ (fps)'][0:26]


# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X256_B1_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP256B1 = columns['TEXP (s)'][0:32]
FREQ256B1 = columns['FREQ (fps)'][0:32]


# In[3]:


# Constroi o modelo para o primeiro regime da curva
fRegime1 = lambda x,a,b: a*x+b

# Faz o ajuste para cada regime, dado o modelo
ncorte = 11
R1popt1024B1, R1pcov1024B1 = curve_fit(fRegime1, TEXP1024B1[:ncorte], FREQ1024B1[:ncorte])
a=-R1popt1024B1[0]
b=-R1popt1024B1[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


ncorte = 6
R1popt512B1, R1pcov512B1 = curve_fit(fRegime1, TEXP512B1[:ncorte], FREQ512B1[:ncorte])
a=-R1popt512B1[0]
b=-R1popt512B1[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


ncorte = 12
R1popt256B1, R1pcov256B1 = curve_fit(fRegime1, TEXP256B1[:ncorte], FREQ256B1[:ncorte])
a=-R1popt256B1[0]
b=-R1popt256B1[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


# In[9]:


fontsize = 14
fig = plt.figure()
ax = fig.add_subplot(111)


ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')

#ax.plot(x1, fRegime1(x1,R1popt[0],R1popt[1]), '-', c='red')
#ax.plot(x2, fRegime2(x2,R2popt), '-', c='red')

plt.xlabel(r'$ Tempo \;\; de \;\; Exposi c \c \tilde{a} o \;\; (s) $', size=fontsize)
plt.ylabel(r'$ Frequ\^ encia \;\; de \;\; aquisic \c \~{a}o \;\; (fps) $', size=fontsize)
plt.rc('xtick', labelsize=13) 
plt.rc('ytick', labelsize=13)
#plt.title(r'$\mathtt{Frequ\^ encia \quad de \quad aquisic \c \~ao \quad em \quad fun c \c \~ao \quad do \quad tempo \quad de \quad exposic \c \~ao}$'+'\n', size=fontsize)
#plt.ylim(1.8, 2.3)
#plt.xlim(-0.02, 0.22)
plt.legend(loc='upper right')

#string = r'$\mathtt{f(x) = } \{ $'+\
#r'$ %.3f \times x + %.3f, \quad x\leq 1,114 $'%(R1popt[0],R1popt[1])+'\n' \
#r'$\quad \quad %.2f/x , \quad  x > 1,114$'%(R2popt)
#ax.text(0.55, 0.9, string, ha='center',va='center', transform=ax.transAxes, size=fontsize)
plt.show()


# In[4]:


# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X1024_B2_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP1024B2 = columns['TEXP (s)'][0:22]
FREQ1024B2 = columns['FREQ (fps)'][0:22]

# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X512_B2_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP512B2 = columns['TEXP (s)'][0:27]
FREQ512B2 = columns['FREQ (fps)'][0:27]


# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel ('C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Acq_Frequency\HSS1MHz\X256_B2_Propagado.xlsm') 
columns = pd.DataFrame(df)
TEXP256B2 = columns['TEXP (s)'][0:30]
FREQ256B2 = columns['FREQ (fps)'][0:30]


# In[6]:


# Constroi o modelo para o primeiro regime da curva
fRegime1 = lambda x,a,b: a*x+b

# Faz o ajuste para cada regime, dado o modelo
ncorte = 6
R1popt1024B2, R1pcov1024B2 = curve_fit(fRegime1, TEXP1024B2[:ncorte], FREQ1024B2[:ncorte])
a=-R1popt1024B2[0]
b=-R1popt1024B2[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


ncorte = 6
R1popt512B2, R1pcov512B2 = curve_fit(fRegime1, TEXP512B2[:ncorte], FREQ512B2[:ncorte])
a=-R1popt512B2[0]
b=-R1popt512B2[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


ncorte = 6
R1popt256B2, R1pcov256B2 = curve_fit(fRegime1, TEXP256B2[:ncorte], FREQ256B2[:ncorte])
a=-R1popt256B2[0]
b=-R1popt256B2[1]
c=1
delta = b**2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
print x2


# In[8]:


fontsize = 14
fig = plt.figure()
ax = fig.add_subplot(111)


ax.errorbar(TEXP256B2, FREQ256B2, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B2}$')
ax.errorbar(TEXP512B2, FREQ512B2, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B2}$')
ax.errorbar(TEXP1024B2, FREQ1024B2, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B2}$')

plt.xlabel(r'$ Tempo \;\; de \;\; Exposi c \c \tilde{a} o \;\; (s) $', size=fontsize)
plt.ylabel(r'$ Frequ\^ encia \;\; de \;\; aquisic \c \~{a}o \;\; (fps) $', size=fontsize)
plt.rc('xtick', labelsize=13) 
plt.rc('ytick', labelsize=13)
#plt.ylim(1.8, 2.3)
#plt.xlim(-0.02, 0.22)
plt.legend(loc='upper right')
plt.show()

