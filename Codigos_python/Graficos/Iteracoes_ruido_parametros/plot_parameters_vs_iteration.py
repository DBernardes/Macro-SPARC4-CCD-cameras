#!/usr/bin/env python
# coding: utf-8

# Este codigo plota os valores do ruido de leitura encontrados
#pela biblioteca hyperopt em funcao do numero de iteracao.

#22/11/2019. Denis Varise Bernardes.

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import json
from sys import exit

##arq = open(r'Logs\Parameters\log.txt', 'r')
##lines_parameters = arq.read().splitlines()
##lines_parameters = [i.split('\t') for i in lines_parameters]
##arq.close()

array_dic_modes=[]
with open(r'Logs\Parameters\log.txt', 'r') as arq:
    lines = arq.read().splitlines()
    for line in lines:        
        dic = json.loads(line)        
        array_dic_modes.append(dic)        
        arq.close()

##arq = open(r'Logs\Loss\log.txt', 'r')
##lines_loss = arq.read().splitlines()
##lines_loss = [float(i) for i in lines_loss[:-1]]
##arq.close()

t_exp = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
em_mode = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
em_gain = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
hss = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
preamp = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
binn = {'0.1':[], '1':[], '10':[], '20':[], '30':[]}
loss ={'0.1':[], '1':[], '10':[], '20':[], '30':[]}


 
for i in range(len(array_dic_modes)):
    dic = array_dic_modes[i]
    #line = [float(i) for i in line]    
    if dic['hss'] == 0.1:
        t_exp['0.1'].append(dic['t_exp'])
        em_mode['0.1'].append(dic['em_mode'])
        em_gain['0.1'].append(dic['em_gain'])
        preamp['0.1'].append(dic['preamp'])
        binn['0.1'].append(dic['binn'])
        loss['0.1'].append(dic['snr'])
    if dic['hss'] == 1:
        t_exp['1'].append(dic['t_exp'])
        em_mode['1'].append(dic['em_mode'])
        em_gain['1'].append(dic['em_gain'])
        preamp['1'].append(dic['preamp'])
        binn['1'].append(dic['binn'])
        loss['1'].append(dic['snr'])
    if dic['hss'] == 10:
        t_exp['10'].append(dic['t_exp'])
        em_mode['10'].append(dic['em_mode'])
        em_gain['10'].append(dic['em_gain'])
        preamp['10'].append(dic['preamp'])
        binn['10'].append(dic['binn'])
        loss['10'].append(dic['snr'])
    if dic['hss'] == 20:
        t_exp['20'].append(dic['t_exp'])
        em_mode['20'].append(dic['em_mode'])
        em_gain['20'].append(dic['em_gain'])
        preamp['20'].append(dic['preamp'])
        binn['20'].append(dic['binn'])
        loss['20'].append(dic['snr'])
    if dic['hss'] == 30:
        t_exp['30'].append(dic['t_exp'])
        em_mode['30'].append(dic['em_mode'])
        em_gain['30'].append(dic['em_gain'])
        preamp['30'].append(dic['preamp'])
        binn['30'].append(dic['binn'])
        loss['30'].append(dic['snr'])


fig = plt.figure()
list_fake2Dlines = []
list_labels = []
ax = fig.add_subplot((111), projection='3d')
if t_exp['30']:
    ax.scatter(t_exp['30'], em_gain['30'], loss['30'], c='blue', marker='o', alpha=0.5)
    fake2Dline1 = mpl.lines.Line2D([0],[0], linestyle="none", c='blue', marker = 'o')
    list_fake2Dlines.append(fake2Dline1)
    list_labels.append(r'30 MHz')
if t_exp['20']:
    ax.scatter(t_exp['20'], em_gain['20'], loss['20'], c='red', marker='o', alpha=0.5)
    fake2Dline2 = mpl.lines.Line2D([0],[0], linestyle="none", c='red', marker = 'o')
    list_fake2Dlines.append(fake2Dline2)
    list_labels.append(r'20 MHz')
if t_exp['10']:
    ax.scatter(t_exp['10'], em_gain['10'], loss['10'], c='green', marker='o', alpha=0.5)
    fake2Dline3 = mpl.lines.Line2D([0],[0], linestyle="none", c='green', marker = 'o')
    list_fake2Dlines.append(fake2Dline3)
    list_labels.append(r'10 MHz')
if t_exp['1']:
    ax.scatter(t_exp['1'], em_gain['1'], loss['1'], c='tab:purple', marker='o', alpha=0.6)
    fake2Dline4 = mpl.lines.Line2D([0],[0], linestyle="none", c='tab:purple', marker = 'o')
    list_fake2Dlines.append(fake2Dline4)
    list_labels.append(r'1 MHz')
if t_exp['0.1']:
    ax.scatter(t_exp['0.1'], em_gain['0.1'], loss['0.1'], c='tab:olive', marker='o', alpha=0.8)
    fake2Dline5 = mpl.lines.Line2D([0],[0], linestyle="none", c='tab:olive', marker = 'o')
    list_fake2Dlines.append(fake2Dline5)
    list_labels.append(r'0,1 MHz')

ax.set_xlabel('Exposure Time (s)')
ax.set_ylabel('EM Gain')
ax.set_zlabel('SNR*FA')
ax.legend(list_fake2Dlines, list_labels, numpoints = 1)
plt.show()


'''
for i in x:
    line = lines_parameters[i]
    binn = 0
    if line[5] == str(2): binn = 1
    if line[4] == str(1):
        t_exp_1[binn].append(float(line[0]))
        em_mode_1[binn].append(float(line[1]))
        em_gain_1[binn].append(float(line[2]))
        hss_1[binn].append(float(line[3]))
        preamp_1[binn].append(float(line[4]))
        binn_1[binn].append(float(line[5]))
        loss_1[binn].append(lines_loss[i])

    else:        
        t_exp_2[binn].append(float(line[0]))
        em_mode_2[binn].append(float(line[1]))
        em_gain_2[binn].append(float(line[2]))
        hss_2[binn].append(float(line[3]))
        preamp_2[binn].append(float(line[4]))
        binn_2[binn].append(float(line[5]))
        loss_2[binn].append(lines_loss[i])
'''
