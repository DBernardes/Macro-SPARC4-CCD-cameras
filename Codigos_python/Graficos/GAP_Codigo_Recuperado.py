#!/usr/bin/env python
# coding: utf-8

# In[17]:


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


df = pd.read_excel (r'C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\GAP_Codigo_Recuperado.xlsx') 
columns = pd.DataFrame(df)


GAP    = {}
GAP['value'] = columns['# Images']
GAP['GAP'] = columns['GAP']
GAP['error'] = columns['Error']
GAP['GAP_IMG'] = columns['GAP/#Image']


fontsize = 15
plt.figure(figsize=(12,5))
plt.subplot2grid((1,2),(0,0))
plt.errorbar(GAP['value'], GAP['GAP'], GAP['error'] , marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{N \acute{u} mero \quad de \quad imagens}$', size=fontsize)
plt.ylabel(r'$\mathtt{GAP \quad (s)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad GAP \quad entre \quad cubos \quad de \quad imagens}$'+'\n', size=fontsize)
#plt.ylim(1.8, 2.3)
plt.xlim(-5, 85)

plt.subplot2grid((1,2),(0,1))
plt.errorbar(GAP['value'], GAP['GAP_IMG'], marker='o', c='blue',linewidth=1.0)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad GAP \quad por \quad imagem}$'+'\n', size=fontsize)
plt.xlabel(r'$\mathtt{N \acute{u} mero \quad de \quad imagens}$', size=fontsize)
plt.ylabel(r'$\mathtt{GAP \backslash Imagem \quad (s)}$', size=fontsize)
#plt.ylim(1.8, 2.3)
plt.xlim(-5, 85)

plt.show()

