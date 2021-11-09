#!/usr/bin/env python
# coding: utf-8

#Classe OptReadNoise criada para a otimizacao do read noise da camera iXon Ultra
#888 atraves da biblioteca hyperopt. Sera usada a classe ReadNoiseCalc
#para fornecer o valor do ruido de leitura para cada modo
#de operacao da camera.
#Denis Varise Bernardes.
#15/10/2019.



import Read_Noise_Calculation_Bib as RNC
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Modos_Operacao_Bib as MOB
import collections
from hyperopt import hp, tpe, Trials, fmin
from hyperopt.pyll.stochastic import sample
from hyperopt.pyll import scope



def function(em_mode=1, em_gain=2, hss=1, preamp=1, binn=1):    
    RN = RNC.ReadNoiseCalc()    
    RN.write_operation_mode(em_mode, em_gain, hss, preamp, binn)
    #RN.get_operation_mode()
    RN.calc_read_noise()
    read_noise = float(RN.noise)
    
    return read_noise

#-------------------------------------------------------------------

class OptReadNoise:

    def __init__(self):
        #self.RN = RNC.ReadNoiseCalc()
        self.MOB = MOB.ModosOperacao()
        self.space = []        
        self.hss = [[],[]]
        self.binn = [[],[]]
        self.sub_img = []
        self.best_mode = {}        
        self.list_all_modes  = []
        self.filtered_list = [] #esta lista foi criada para filtrar os modos repetidos da list_all_modes
        self.best_sub_img = []

    def write_MOB_obj(self, obj):
        self.MOB = obj


    def get_list_of_modes(self):
        return self.MOB.modos_operacao


    def print_MOB_list(self):
        for modo in self.get_list_of_modes():
            print(modo)
            

    def create_list_allowed_modes(self):
        #Acho que eu não utilizo mais esta função!!!
        for mode in self.list_all_modes:
            #Caso o novo modo nao esteja na lista, ele eh adicionado
            em_mode =  mode['em_mode'] # esta variavel faz a separacao para qual subarray o novo modo vai
            if mode['hss'] not in self.hss[em_mode]:
                self.hss[em_mode].append(mode['hss'])
            if mode['binn'] not in self.binn[em_mode]:
                self.binn[em_mode].append(mode['binn'])


    def create_space(self):
        #O variavel filtered_list elimina a adicao repetida dos modos selecionados por opttimize_acquisition_rate
        # em funcao dos sug_imgs permitidos, ou seja, uma mesmo modo pode aparecer mais que uma vez caso ele
        # possua os valores de sub_img x256 e x512.
        self.list_all_modes = self.get_list_of_modes() #Cria uma lista dos modos permitidos
        for mode in self.list_all_modes:
            new_mode = {'em_mode':mode['em_mode'], 'hss':mode['hss'], 'binn':mode['binn']}
            if new_mode not in self.filtered_list: self.filtered_list.append(new_mode)        

        i=0
        space_all_modes = []
        #Este loop transforma cada modo selecinado pelo opttimize_acquisition_rate no formato do espaço de
        # estados da funcao hyperopt. Entao, cada modo eh passado para uma lista space_all_modes que, por sua vez,
        # eh fornecida para a funcao hp.choice. Isso evita a selecao de modos nao permitidos durante a otimizacao.
        for mode in self.filtered_list:           
            em_mode = hp.choice('em_mode_' + str(i), [mode['em_mode']])
            if mode['em_mode'] == 0:
                em_gain = hp.choice('em_gain_'+ str(i), [0]) #como o ganho nao tem influencia para emo_mode=0, eu forco o zero.
            else:
                em_gain = hp.uniform('em_gain_'+ str(i), 2, 300)
            hss     = hp.choice('hss_' + str(i), [mode['hss']])
            preamp  = hp.choice('preamp_' + str(i), [1,2])       
            binn    = hp.choice('binn_' + str(i), [mode['binn']])
            new_mode = [em_mode, em_gain, hss, preamp, binn]            
            space_all_modes.append(new_mode)
            i+=1        
        self.space = hp.choice('operation_mode', space_all_modes)        
    

    def run_bayesian_opt(self, max_evals):
        
        # Create the algorithm
        tpe_algo = tpe.suggest

        # Create a trials object
        self.tpe_trials = Trials()

        # Run evals with the tpe algorithm
        best_mode  = fmin(fn=function, space=self.space, algo=tpe_algo, trials=self.tpe_trials, max_evals=max_evals, rstate= np.random.RandomState(50))
        #print(best_mode)
        
        index_list_modes = next(iter(best_mode)).split('_')[-1]
        chosen_mode = self.filtered_list[int(index_list_modes)]
        
        em_mode = chosen_mode['em_mode']
        em_gain = best_mode['em_gain_' + index_list_modes]
        hss = chosen_mode['hss']
        preamp = best_mode['preamp_' + index_list_modes]+1
        binn = chosen_mode['binn']
        self.best_mode = {'em_mode':em_mode, 'em_gain':em_gain,'hss':hss, 'preamp':preamp,'binn':binn, 'noise':self.tpe_trials.best_trial['result']['loss']}
        #print(self.tpe_trials.idxs_vals[1])


    def creat_log_parameters(self):
        # neste loop eh criado um arquivo contendo o log dos parametros utilizados em cada itercao do MOB.
        # como podem haver valores repetidos, a lista dos valores utilizados precisa ser dividida entre
        # os casos que aparecem uma unica vez e aqueles que aparecem duas ou mais. Os casos que aparecem
        # duas ou mais vezes precisam passar por um novo loop para separar cada modo utilizado
        opt_log = self.tpe_trials.idxs_vals[1]
        op_modes_list = opt_log['operation_mode']
        arq = open(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\Graficos\Iteracoes_ruido_parametros\parameters_log.txt', 'w')
        for item, count in collections.Counter(op_modes_list).items():            
            mode = self.filtered_list[item]
            hss = mode['hss']
            em_mode = mode['em_mode']
            binn = mode['binn']
            if count == 1:
                s=''
                em_gain = opt_log['em_gain_' + str(item)][0]                
                preamp = opt_log['preamp_' + str(item)][0]+1
                s += str(em_mode) + '\t' + str(em_gain) + '\t' + str(hss) + '\t' + str(preamp) + '\t' + str(binn)
                arq.write(s + '\n')
            else:
                for i in range(count):
                    s=''
                    em_gain = opt_log['em_gain_' + str(item)][i]
                    preamp = opt_log['preamp_' + str(item)][i] + 1
                    s += str(em_mode) + '\t' + str(em_gain) + '\t' + str(hss) + '\t' + str(preamp) + '\t' + str(binn)
                    arq.write(s + '\n')
        arq.close()
                    


    def creat_log_loss(self):           
        arq = open(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\Graficos\Iteracoes_ruido_parametros\loss_log.txt', 'w')        
        for x in self.tpe_trials.results:
            arq.write(str(x['loss']))
            arq.write('\n')
        arq.close()



    def find_sub_img_best_mode(self):
        for mode in self.list_all_modes:
            if mode['em_mode'] == self.best_mode['em_mode']:
                if mode['hss'] == self.best_mode['hss']:
                    if mode['binn'] == self.best_mode['binn']:
                        self.best_sub_img.append(mode['sub_img'])
            
        
    

    def print_best_mode(self):                 
        if self.best_mode['em_mode'] == 1:
            print('\nEM Mode')
            print('-------')
            print('EM gain: ', self.best_mode['em_gain'])
            print('HSS: ', self.best_mode['hss'])
            print('Preamp: ', self.best_mode['preamp'])
            print('Binning: ', self.best_mode['binn'])
            print('Sub image: ', max(self.best_sub_img))
            print('\nBest Noise (e-): ', self.best_mode['noise'])

        else:
            print('\nConventional Mode')
            print('-----------------')
            print('HSS: ', self.best_mode['hss'])
            print('Preamp: ', self.best_mode['preamp'])
            print('Binning: ', self.best_mode['binn'])
            print('Sub image: ', max(self.best_sub_img))
            print('\nBest Noise (e-): ',  self.best_mode['noise'])

            
