#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit



#----------------- 0.1 MHz, B1 --------------------------------------------------------------
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B1HSS01.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:22]
##FREQ1024B1 = columns['FREQ (fps)'][0:22]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B1HSS01.xlsm') 
##columns = pd.DataFrame(df)
##TEXP512B1 = columns['TEXP (s)'][0:27]
##FREQ512B1 = columns['FREQ (fps)'][0:27]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B1HSS01.xlsm') 
##columns = pd.DataFrame(df)
##TEXP256B1 = columns['TEXP (s)'][0:23]
##FREQ256B1 = columns['FREQ (fps)'][0:23]
##
##fontsize = 14
fig = plt.figure()
##ax = fig.add_subplot(251)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('0.1 MHz B1')

#----------------- 0.1 MHz, B2 --------------------------------------------------------------

##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B2HSS01.xlsm') 
##columns = pd.DataFrame(df)
##
##TEXP1024B2 = columns['TEXP (s)'][0:19]
##FREQ1024B2 = columns['FREQ (fps)'][0:19]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B2HSS01.xlsm') 
##columns = pd.DataFrame(df)
##TEXP512B2 = columns['TEXP (s)'][0:23]
##FREQ512B2 = columns['FREQ (fps)'][0:23]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B2HSS01.xlsm') 
##columns = pd.DataFrame(df)
##TEXP256B2 = columns['TEXP (s)'][0:19]
##FREQ256B2 = columns['FREQ (fps)'][0:19]
##
##ax = fig.add_subplot(252)
##ax.errorbar(TEXP256B2, FREQ256B2, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B2}$')
##ax.errorbar(TEXP512B2, FREQ512B2, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B2}$')
##ax.errorbar(TEXP1024B2, FREQ1024B2, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B2}$')
##plt.title('0.1 MHz B2')
#----------------- 1 MHz, B1 --------------------------------------------------------------

# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B1HSS1.xlsm') 
columns = pd.DataFrame(df)
TEXP1024B1 = columns['TEXP (s)'][0:21]
FREQ1024B1 = columns['FREQ (fps)'][0:21]

# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B1HSS1.xlsm') 
columns = pd.DataFrame(df)
TEXP512B1 = columns['TEXP (s)'][0:26]
FREQ512B1 = columns['FREQ (fps)'][0:26]


# Faz a leitura da planilha e pega os valores das colunas
df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B1HSS1.xlsm') 
columns = pd.DataFrame(df)
TEXP256B1 = columns['TEXP (s)'][0:32]
FREQ256B1 = columns['FREQ (fps)'][0:32]

ax = fig.add_subplot(111)
ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256}$')
ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512}$')
ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024}$')
ax.legend()
#plt.title('1 MHz B1')
plt.show()
###----------------- 1 MHz, B2 --------------------------------------------------------------
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B2HSS1.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B2 = columns['TEXP (s)'][0:22]
##FREQ1024B2 = columns['FREQ (fps)'][0:22]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B2HSS1.xlsm') 
##columns = pd.DataFrame(df)
##TEXP512B2 = columns['TEXP (s)'][0:27]
##FREQ512B2 = columns['FREQ (fps)'][0:27]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B2HSS1.xlsm') 
##columns = pd.DataFrame(df)
##TEXP256B2 = columns['TEXP (s)'][0:30]
##FREQ256B2 = columns['FREQ (fps)'][0:30]
##
##ax = fig.add_subplot(254)
##ax.errorbar(TEXP256B2, FREQ256B2, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B2}$')
##ax.errorbar(TEXP512B2, FREQ512B2, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B2}$')
##ax.errorbar(TEXP1024B2, FREQ1024B2, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B2}$')
##plt.title('1 MHz B2')
###----------------- 10 MHz, B1 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B1HSS10.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:16]
##FREQ1024B1 = columns['FREQ (fps)'][0:16]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B1HSS10.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:31]
##FREQ512B1 = columns['FREQ (fps)'][0:31]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B1HSS10.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:25]
##FREQ256B1 = columns['FREQ (fps)'][0:25]
##
##ax = fig.add_subplot(255)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('10 MHz B1')
###----------------- 10 MHz, B2 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B2HSS10.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:16]
##FREQ1024B1 = columns['FREQ (fps)'][0:16]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B2HSS10.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:31]
##FREQ512B1 = columns['FREQ (fps)'][0:31]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B2HSS10.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:25]
##FREQ256B1 = columns['FREQ (fps)'][0:25]
##
##ax = fig.add_subplot(256)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('10 MHz B2')
###----------------- 20 MHz, B1 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B1HSS20.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:31]
##FREQ1024B1 = columns['FREQ (fps)'][0:31]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B1HSS20.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:25]
##FREQ512B1 = columns['FREQ (fps)'][0:25]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B1HSS20.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:26]
##FREQ256B1 = columns['FREQ (fps)'][0:26]
##
##ax = fig.add_subplot(257)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('20 MHz B1')
###----------------- 20 MHz, B2 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B2HSS20.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:25]
##FREQ1024B1 = columns['FREQ (fps)'][0:25]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B2HSS20.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:26]
##FREQ512B1 = columns['FREQ (fps)'][0:26]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B2HSS20.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:31]
##FREQ256B1 = columns['FREQ (fps)'][0:31]
##
##ax = fig.add_subplot(258)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('20 MHz B2')
###----------------- 30 MHz, B1 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B1HSS30.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:15]
##FREQ1024B1 = columns['FREQ (fps)'][0:15]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B1HSS30.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:16]
##FREQ512B1 = columns['FREQ (fps)'][0:16]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B1HSS30.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:26]
##FREQ256B1 = columns['FREQ (fps)'][0:26]
##
##ax = fig.add_subplot(259)
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('30 MHz B1')
###----------------- 30 MHz, B2 --------------------------------------------------------------
##
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X1024B2HSS30.xlsm') 
##columns = pd.DataFrame(df)
##TEXP1024B1 = columns['TEXP (s)'][0:25]
##FREQ1024B1 = columns['FREQ (fps)'][0:25]
##
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X512B2HSS30.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP512B1 = columns['TEXP (s)'][0:31]
##FREQ512B1 = columns['FREQ (fps)'][0:31]
##
### Faz a leitura da planilha e pega os valores das colunas
##df = pd.read_excel(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\blibioteca_de_funcoes\X256B2HSS30.xlsm') 
##columns = pd.DataFrame(df)
##Freq    = {}
##TEXP256B1 = columns['TEXP (s)'][0:33]
##FREQ256B1 = columns['FREQ (fps)'][0:33]
##
##ax = plt.subplot2grid((2,5), (1, 4))
##ax.errorbar(TEXP1024B1, FREQ1024B1, marker='o', c='blue',linewidth=1.0, label=r'$\mathtt{x1024, \; B1}$')
##ax.errorbar(TEXP512B1, FREQ512B1, marker='o', c='red',linewidth=1.0, label=r'$\mathtt{x512, \; B1}$')
##ax.errorbar(TEXP256B1, FREQ256B1, marker='o', c='green',linewidth=1.0, label=r'$\mathtt{x256, \; B1}$')
##plt.title('30 MHz B2')
##
###plt.xlim(0,20)
###plt.xlabel(r'$ Tempo \;\; de \;\; Exposi c \c \tilde{a} o \;\; (s) $', size=fontsize)
###plt.ylabel(r'$ Frequ\^ encia \;\; de \;\; aquisic \c \~{a}o \;\; (fps) $', size=fontsize)
##plt.rc('xtick', labelsize=13) 
##plt.rc('ytick', labelsize=13)
##plt.legend(loc='upper right')
##plt.show()

