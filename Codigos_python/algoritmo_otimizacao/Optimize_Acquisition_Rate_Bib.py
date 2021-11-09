#!/usr/bin/env python
# coding: utf-8

# Classe OptimizeAcquisitionRate criada para determinar os modos de opercao que atendem ao
# requisito cientifico da frequencia de aquisicao da camera iXon Ultra 888. Este codigo
# utiliza da biblioteca Acquisition_Rate_Calculation_Bib para retornar o valor da
# frequencia de aquisicao para um dado modo e, entao, decide se este modo pode ser
# utilizado. Os modos selecionado sao escritos dentro da classe Modos_Operacao_Bib
# e, entao, esta classe eh passada para a rotina de determinacao do modo de operacao
# do ruido otimo.

#24/10/2019. Denis Varise Bernardes.

import Modos_Operacao_Bib as MOB
import Acquisition_Rate_Calculation_Bib as arc
import os
from hyperopt import hp, tpe, rand, Trials, fmin
from sys import exit
import numpy as np
import json
def function(parameters = []):      
    exp_time = parameters[0]
    em_mode = parameters[1]
    hss = parameters[2]    
    binn = parameters[3]
    sub_img = parameters[4]    

    ARC = arc.AcquisitionRateCalc()
    ARC.write_operation_mode(em_mode, hss, binn, sub_img, exp_time)
    ARC.seleciona_t_corte()
    ARC.calc_acquisition_rate()
    acq_rate = ARC.acquisition_rate
    
    return -acq_rate

class OptimizeAcquisitionRate:

    def __init__(self, acquisition_rate, sub_img_modes, binn_modes):        
        # objeto que ira armazenare os dados selecionados
        self.MOB = MOB.ModosOperacao()
        #objeto da funcao que calcula a taxa de aquisicao
        self.ARC = arc.AcquisitionRateCalc()        
        self.acquisition_rate = acquisition_rate
        self.vector_sub_img = sub_img_modes
        self.vector_binn = binn_modes
        self.t_exp = 0.00001
        self.best_mode = {}


    def write_mode_to_MOB_class(self, em_mode, em_gain, hss, preamp, binn, sub_img, t_exp):
        #Escreve os modos selecinados em uma lista de dicionarios
        self.MOB.write_mode(em_mode, em_gain, hss, preamp, binn, sub_img, t_exp)
         
    def print_MOB_list(self):        
        lista =  self.MOB.get_list_of_modes()
        for modo in lista:
            print(modo)

    def write_MOB_obj(self, obj):
        self.MOB = obj

    def read_MOB_obj(self):
        return self.MOB

    
    def determine_operation_modes(self):
        vector_em = [0, 1]        
        for em_mode in vector_em:
            vector_hss = [1, 10, 20, 30]
            if em_mode == 0: vector_hss = [0.1, 1]
            
            for hss in vector_hss:
                for binn in self.vector_binn:
                    for sub_img in self.vector_sub_img:                    
                        self.ARC.write_operation_mode(em_mode, hss, binn, sub_img, self.t_exp)
                        self.ARC.seleciona_t_corte()
                        self.ARC.calc_acquisition_rate()
                        #print(self.ARC.acquisition_rate, self.acquisition_rate)
                        if self.ARC.acquisition_rate >= self.acquisition_rate:
                            max_t_exp = self.ARC.calc_texp_provided_acquisition_frequency(self.acquisition_rate)                            
                            self.write_mode_to_MOB_class(em_mode, 0, hss, 0, binn, sub_img, max_t_exp)




    #Esta função encontra qual o modo de operação mais rápido dentre uma lista de modos fornecida.    
    def determine_fastest_operation_mode(self):
        max_acq_rate = 0
        best_mode = {}               
        for mode in self.MOB.get_list_of_modes():
            self.ARC.write_operation_mode(mode['em_mode'], mode['hss'], mode['binn'],  mode['sub_img'], mode['min_t_exp']) 
            self.ARC.seleciona_t_corte()
            self.ARC.calc_acquisition_rate()
            #print(self.ARC.acquisition_rate)
            if self.ARC.acquisition_rate > max_acq_rate:
                max_acq_rate = self.ARC.acquisition_rate                
                self.best_mode = mode    
                self.best_mode['max_acq_rate'] = max_acq_rate
            #Esta sequência de ifs serve para o caso onde a taxa de aquisição é a mesma para modos sub_img diferentes
            #Logo, o ideal é usar o sub_img maior.
            if self.ARC.acquisition_rate == max_acq_rate:
                if mode['hss'] == self.best_mode['hss']:
                    if mode['em_mode'] == self.best_mode['em_mode']:
                        if mode['binn'] == self.best_mode['binn']:
                            if mode['sub_img'] > self.best_mode['sub_img']:
                                self.best_mode['sub_img'] = mode['sub_img']
                    
                                


    #Esta função encontra qual o modo de operação mais rápido dentre uma lista de modos fornecida.    
    def determine_fastest_operation_mode_2(self):
        max_acq_rate = 0
        best_mode = {}
        # Neste primeiro loop eu fixo um sub_img e encontro o modo mais rápido        
        for mode in self.MOB.get_list_of_modes():
            self.ARC.write_operation_mode(mode['em_mode'], mode['hss'], mode['binn'], max(self.vector_sub_img), mode['min_t_exp']) 
            self.ARC.seleciona_t_corte()
            self.ARC.calc_acquisition_rate()
            if self.ARC.acquisition_rate > max_acq_rate:
                max_acq_rate = self.ARC.acquisition_rate
                best_mode = mode
        best_mode['sub_img'] = 1024  
        # Neste segundo loop eu encontro o maior sub_img que posso utilizar para a aquisição.
        # Faço isso porque as vezes não dá diferença nenhuma utilizar um sub_img de 1024x ou 256x.
        for sub_img in self.vector_sub_img:
            self.ARC.write_operation_mode(best_mode['em_mode'], best_mode['hss'], best_mode['binn'], sub_img, best_mode['min_t_exp'])
            self.ARC.seleciona_t_corte()
            self.ARC.calc_acquisition_rate()
            if self.ARC.acquisition_rate > max_acq_rate:
                max_acq_rate = self.ARC.acquisition_rate
                best_mode['sub_img'] = sub_img       
        best_mode['max_acq_rate'] = max_acq_rate        
        self.best_mode = best_mode


    def create_space(self):       
        i=0
        space_all_modes = []
        #Este loop transforma cada modo selecinado no formato do espaço de
        # estados da funcao hyperopt. Entao, é passado para uma lista space_all_modes que, por sua vez,
        # eh passada para a funcao hp.choice. Isso evita a selecao de modos nao permitidos durante a otimizacao.        
        for mode in self.MOB.get_list_of_modes():
            #t_exp   = hp.choice('t_exp_' + str(i), [0.00001])
            t_exp   = hp.uniform('t_exp_' + str(i), mode['min_t_exp'], mode['max_t_exp'])
            em_mode = hp.choice('em_mode_' + str(i), [mode['em_mode']])            
            hss     = hp.choice('hss_' + str(i), [mode['hss']])            
            binn    = hp.choice('binn_' + str(i), [mode['binn']])          
            sub_img = hp.choice('sub_img_' + str(i),[mode['sub_img']])                          
            new_mode = [t_exp, em_mode, hss, binn, sub_img] 
            space_all_modes.append(new_mode)
            i+=1        
        self.space = hp.choice('operation_mode', space_all_modes)


    def run_bayesian_opt(self, max_evals, algorithm=tpe.suggest):
        # Create the algorithm
        algo = algorithm

        # Create a trials object
        self.tpe_trials = Trials()

        # Run evals with the tpe algorithm
        best_mode  = fmin(fn=function, space=self.space, algo=algo, trials=self.tpe_trials, max_evals=max_evals, rstate= np.random.RandomState(50))               
        


    def print_best_mode(self):                 
        if self.best_mode['em_mode'] == 1:
            print('\nEM Mode')
            print('-------')
            print('EM gain: ', self.best_mode['em_gain'])
        else:
            print('\nConventional Mode')
            print('-----------------')            
        print('Exposure time (s): ', self.best_mode['min_t_exp'])            
        print('HSS: ', self.best_mode['hss'])
        print('Preamp: ', self.best_mode['preamp'])
        print('Binning: ', self.best_mode['binn'])        
        print('Sub image: ', self.best_mode['sub_img'])
        print('\nBest Acquisition Rate: ', self.best_mode['max_acq_rate'])
        if self.best_mode['max_acq_rate'] < self.acquisition_rate: print('\nIt was not possible to reach the acquisition rate')


    def export_optimal_setup(self, img_directory):        
        dic={}        
        if self.best_mode['em_mode'] == 1:
            dic['em_mode'] = 'EM Mode'
            dic['em_gain'] = self.best_mode['em_gain']
        else:
            dic['em_mode'] = 'Conventional Mode'
        dic['t_exp'] = self.best_mode['min_t_exp']
        dic['hss'] = self.best_mode['hss']
        dic['preamp'] = self.best_mode['preamp']
        dic['bin'] = self.best_mode['binn']
        dic['sub_img'] = self.best_mode['sub_img']
        dic['FA'] = float(self.best_mode['max_acq_rate'])
        
        if img_directory!= '': os.chdir(img_directory)
        file_name = 'conv_'
        if self.best_mode['em_mode'] == 1: file_name='EM_'
        file_name+= str(self.best_mode['hss']) + 'MHz_' + 'PA' + str(self.best_mode['preamp']) + '_B' + str(self.best_mode['binn']) + '_SI' + str(self.best_mode['sub_img']) + '.txt'
        
        with open(file_name, 'w') as arq:
            json.dump(dic, arq, indent = 4, sort_keys=True)
            arq.close()                  




##     def determine_operation_modes2(self):
##        # Varre os modos Conv        
##        vector_hss = [0.1, 1]        
##        for hss in vector_hss:
##            for binn in self.vector_binn:
##                for sub_img in self.vector_sub_img:                    
##                    self.ARC.write_operation_mode(0, hss, binn, sub_img, self.t_exp)
##                    self.ARC.calc_acquisition_rate()
##                    #print(self.ARC.acquisition_rate, self.acquisition_rate)
##                    if self.ARC.acquisition_rate >= self.acquisition_rate:                            
##                        self.write_mode_to_MOB_class(0, 0, hss, 0, binn, sub_img, self.t_exp)
                        
    
##        #Varre os modos EM        
##        vector_hss = [1, 10, 20, 30]        
##        for hss in vector_hss:
##            for binn in self.vector_binn:
##                for sub_img in self.vector_sub_img:                    
##                    self.ARC.write_operation_mode(1, hss, binn, sub_img, self.t_exp)
##                    self.ARC.calc_acquisition_rate()
##                    # Se o valor encontrado > taxa minima
##                    if self.ARC.acquisition_rate >= self.acquisition_rate:
##                        # Adiciona o modo ao objeto MOB                            
##                        self.write_mode_to_MOB_class(1, 0, hss, 0, binn, sub_img, self.t_exp)
##
