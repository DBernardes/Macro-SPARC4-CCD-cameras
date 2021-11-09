#!/usr/bin/env python
# coding: utf-8

# Este codigo plota os valores do ruido de leitura encontrados
#pela biblioteca hyperopt em funcao do numero de iteracao.

#22/11/2019. Denis Varise Bernardes.

import matplotlib.pyplot as plt

arq = open('Logs/Loss/FA50_MAG_8_SNR5_1000it.txt', 'r')
lines = arq.read().splitlines()
arq.close()

losses = [float(i) for i in lines[:-1]]
x = range(1,len(lines))
plt.scatter(x, losses, c='b', marker = 'o', alpha=0.5)
plt.plot(x, losses, c='b', alpha=0.5, linewidth=0.5)
plt.xlabel(r'Iteração')
plt.ylabel(r'Ruído de Leitura (e-)')
plt.title(r'Gráfico do ruído de leitura do CCD em função' + '\n' + 'do número de iterações do MOB')
bbox_props = dict(boxstyle="round,pad=0.3", fc="whitesmoke", ec="k", lw=1)
plt.annotate('Best loss: %s'%(lines[-1].split(':')[1]),
            ha="center", va="center", alpha=0.5, color='k',
            size=15,
            bbox=bbox_props,
            xy=(0.75, 0.65), xycoords='axes fraction',            
            )
plt.show()
