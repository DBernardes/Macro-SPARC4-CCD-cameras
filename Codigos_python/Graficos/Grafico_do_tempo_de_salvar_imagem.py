#!/usr/bin/env python
# coding: utf-8

# Código para gerar o gráfico do tempo de salvar uma imagem em função do número de imagens

# In[11]:




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit






df = pd.read_excel (r'C:\Users\observer\Desktop\Ensaios_e_Caracterizacoes\Planilhas\Grafico_do_tempo_de_salvar_imagem.xlsx') 
columns = pd.DataFrame(df)
#print columns


GAP    = {}
GAP['value'] = columns['Sub Image'][3:9]
GAP['GAP'], GAP['erro'] = splitPlusMinus(columns['Unnamed: 4'][3:9], 3)

f = lambda x,a,b: a*x**2 +b
popt, pcov = curve_fit(f, GAP['value'], GAP['GAP'])
x = np.array([32, 64, 128, 256, 512, 1024])



fontsize = 15
plt.errorbar(GAP['value'], GAP['GAP'], GAP['erro'],  marker='o', c='blue',linewidth=1.0)
plt.plot(x, f(x, *popt), 'r--')
plt.xlabel(r'$\mathtt{N \acute{u} mero \quad de \quad imagens}$', size=fontsize)
plt.ylabel(r'$\mathtt{GAP \quad (s)}$', size=fontsize)
plt.title(r'$\mathtt{Gr \acute{a}fico \quad do \quad GAP \quad entre \quad cubos \quad de \quad imagens \quad sem \quad salvar}$'+'\n', size=fontsize)
#plt.ylim(1.8, 2.3)
plt.xlim(-5, 1050)
plt.show()


