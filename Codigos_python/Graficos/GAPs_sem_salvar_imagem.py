#!/usr/bin/env python
# coding: utf-8

# In[28]:


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


df = pd.read_excel (r'C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\GAPs_sem_salvar_imagem.xlsx') 
columns = pd.DataFrame(df)
#print columns


GAP    = {}
GAP['value'] = [1, 10, 20, 40, 80]
GAP['GAP'] = [columns['#1'][19], columns['#10'][19], columns['#20'][19], columns['#40'][19], columns['#80'][19]]
GAP['error'] = [columns['#1'][20], columns['#10'][20], columns['#20'][20], columns['#40'][20], columns['#80'][20]]


fontsize = 15
plt.errorbar(GAP['value'], GAP['GAP'], GAP['error'], marker='o', c='blue',linewidth=1.0)
plt.xlabel(r'$\mathtt{N \acute{u} mero \quad de \quad imagens}$', size=fontsize)
plt.ylabel(r'$\mathtt{GAP \quad (s)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad GAP \quad entre \quad cubos \quad de \quad imagens \quad sem \quad salvar}$'+'\n', size=fontsize)
#plt.ylim(1.8, 2.3)
plt.xlim(-5, 85)
plt.show()

