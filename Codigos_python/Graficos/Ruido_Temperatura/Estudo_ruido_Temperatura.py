#!/usr/bin/env python
# coding: utf-8

# # Estudo_ruido_Temperatura

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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


df = pd.read_excel (r'C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Estudo_ruido_Temperatura.xlsx') 
columns = pd.DataFrame(df)

temp    = {}
temp['value'] = columns['Temperature']
temp['noise'] = columns['Noise']
temp['error'] = columns['Error']


fontsize = 15
plt.errorbar(temp['value'], temp['noise'], marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{Temperatura (^oC)}$', size=fontsize)
plt.ylabel(r'$\mathtt{Ru \acute{\i} do (ADU)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad ru \acute{\i} do \quad em \quad func\c \tilde{a} o \quad da \quad temperatura}$', size=fontsize)
plt.ylim(15.2, 16.2)
plt.xlim(-65, -5)
plt.show()


# In[ ]:




