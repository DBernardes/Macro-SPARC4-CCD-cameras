#!/usr/bin/env python
# coding: utf-8

#Classe OptSNRAR criada para a otimizacao da relacao sinal-ruído e da frequência de aquisição da camera iXon Ultra
#888 atraves da biblioteca hyperopt. Sera usada a classe SNRCalc e ARCalc
#para fornecer o valor do SNR e da FA para cada modo
#de operacao da camera avaliado.
#Denis Varise Bernardes.
#15/01/2020.


import SNR_Calculation_Bib as snrc
import Optimize_Acquisition_Rate_Bib as oar
import Optimize_Signal_Noise_Ratio_Bib as osnr
import Acquisition_Rate_Calculation_Bib as arc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Modos_Operacao_Bib as mob
import collections
import json
from sys import exit
from hyperopt import hp, tpe, rand, Trials, fmin
from hyperopt.pyll.stochastic import sample
from hyperopt.pyll import scope
from copy import copy
import gc, os
import random as rd




def function_fa(parameters = []):    
    t_exp = parameters[0]
    em_mode = parameters[1]
    em_gain = parameters[2]
    hss = parameters[3]
    preamp = parameters[4]
    binn = parameters[5]
    sub_img = parameters[6]
    CCD_temp = parameters[7]
    sky_flux = parameters[8]
    star_flux = parameters[9]
    n_pixels_star = parameters[10]
    serial_number = parameters[11]    
    mean_fa = parameters[13]        

    ARC = arc.AcquisitionRateCalc()
    ARC.write_operation_mode(em_mode, hss, binn, sub_img, t_exp)
    ARC.seleciona_t_corte()
    ARC.calc_acquisition_rate()
    acq_rate = ARC.acquisition_rate  
    #norm_acq_rate = (acq_rate - mean_fa)/std_fa + 3*offset_fa
    norm_acq_rate = acq_rate/mean_fa
    #norm_acq_rate = acq_rate
    return norm_acq_rate

def function_snr(parameters = []):    
    t_exp = parameters[0]
    em_mode = parameters[1]
    em_gain = parameters[2]
    hss = parameters[3]
    preamp = parameters[4]
    binn = parameters[5]
    sub_img = parameters[6]
    ccd_temp = parameters[7]
    sky_flux = parameters[8]
    star_flux = parameters[9]
    n_pix_star = parameters[10]
    serial_number = parameters[11]
    mean_snr = parameters[12]    
    snr_target = parameters[14]    
    SNRC = snrc.SignalToNoiseRatioCalc(t_exp = t_exp,
                              em_mode = em_mode,
                              em_gain = em_gain,
                              hss = hss,
                              preamp = preamp,
                              binn = binn,
                              ccd_temp = ccd_temp,
                              sky_flux = sky_flux,
                              star_flux = star_flux,
                              n_pix_star = n_pix_star,
                              serial_number = serial_number)    
    SNRC.calc_RN()
    SNRC.calc_DC()
    SNRC.calc_SNR()
    snr = SNRC.get_SNR()
    
    if snr < snr_target: snr = 0
    
    #norm_snr = snr
    #norm_snr = (snr - mean_snr)/std_snr + 3*offset_snr
    norm_snr = snr/mean_snr
    return norm_snr


def function(parameters = []):
    return -function_snr(parameters)*function_fa(parameters)


#-------------------------------------------------------------------

class Opt_SignalNoiseRatio_AcquisitionRate:

    def __init__(self, snr_target, acq_rate, sub_img_modes, binn_modes, serial_number, ccd_temp, n_pix_star, sky_flux, star_flux):                       
        self.hss = [[],[]]
        self.binn = [[],[]]
        self.sub_img = []        
        self.ccd_temp = ccd_temp
        self.serial_number = serial_number
        self.gain = 0 #preamp gain
        self.dark_noise = 0
        self.set_dc() #função para setar a corrente de escuro        
        self.binn_modes = binn_modes
        self.sub_img_modes = sub_img_modes

        self.sky_flux = sky_flux #e-/pix/s                
        self.star_flux = star_flux #e-/s        
        self.n_pix_star = n_pix_star
        
        self.best_mode = {}
        self.space = []         
        self.list_all_modes  = []        
        self.best_sub_img = []        
        self.acq_rate_target = acq_rate
        self.snr_target = snr_target #esta é a snr desejada
        self.losses_SNR = 0
        self.losses_FA = 0
        self.MOB = mob.ModosOperacao()
        self.mean_snr = 0
        self.std_snr = 0
        self.mean_fa = 0
        self.std_fa = 0
        self.space_all_modes=[]
        self.new_list = []
        
    def set_gain(self, em_mode, hss, preamp):
        gain = 0
        if em_mode == 1:
            if hss == 30:
                if preamp == 1:
                    gain = 17.2
                if preamp == 2:
                    gain = 5.27
            if hss == 20:
                if preamp == 1:
                    gain = 16.4
                if preamp == 2:
                    gain = 4.39
            if hss == 10:
                if preamp == 1:
                    gain = 16.0
                if preamp == 2:
                    gain = 3.96
            if hss == 1:
                if preamp == 1:
                    gain = 15.9
                if preamp == 2:
                    gain = 3.88
        else:
            if hss == 1:
                if preamp == 1:
                    gain = 3.37
                if preamp == 2:
                    gain = 0.8
            if hss == 0.1:
                if preamp == 1:
                    gain = 3.35
                if preamp == 2:
                    gain = 0.8
        self.gain = gain  



    def set_dc(self):
         #equacao tirada do artigo de caract. dos CCDs
        T = self.ccd_temp
        if self.serial_number == 9914:
            self.dark_noise = 24.66*np.exp(0.0015*T**2+0.29*T) 
        if self.serial_number == 9915:
            self.dark_noise = 35.26*np.exp(0.0019*T**2+0.31*T)
        if self.serial_number == 9916:
            self.dark_noise = 9.67*np.exp(0.0012*T**2+0.25*T)
        if self.serial_number == 9917:
            self.dark_noise = 5.92*np.exp(0.0005*T**2+0.18*T) 


    def write_MOB_obj(self, obj):
        self.MOB = obj       

   
    def print_MOB_list(self):        
        lista = self.MOB.get_list_of_modes()        
        for modo in lista:
            print(modo)  



    def SNR_FA_ranges(self):        
        #cria o objeto da classe que encontra os modos de SNR permitidos
        OSNR = osnr.OptSignalNoiseRation(serial_number = self.serial_number,
                                         snr_target = 0,# para este caso, precisa ser zero. Se não, a média fica viesada.
                                         ccd_temp = self.ccd_temp,
                                         n_pix_star = self.n_pix_star,
                                         sky_flux = self.sky_flux,
                                         star_flux = self.star_flux)        
        OSNR.write_MOB_obj(self.MOB)
        #OSNR.print_MOB_list(),exit()
        OSNR.filtered_list = self.MOB.get_list_of_modes()
        OSNR.create_space()        
        OSNR.run_bayesian_opt(max_evals=50, algorithm = rand.suggest)
        self.losses_SNR = [-x['loss'] for x in OSNR.tpe_trials.results]
        
        
        OAR =  oar.OptimizeAcquisitionRate(acquisition_rate = self.acq_rate_target,
                                           sub_img_modes=self.sub_img_modes,
                                           binn_modes=self.binn_modes)
        OAR.write_MOB_obj(self.MOB)        
        #OAR.print_MOB_list(),exit()
        OAR.create_space()
        OAR.run_bayesian_opt(max_evals=50, algorithm = rand.suggest)
        self.losses_FA = [-x['loss'] for x in OAR.tpe_trials.results]
        #print(self.losses_SNR, self.losses_FA),exit()
        


    def create_space(self):       
        i=0
        #Fiz esta lista porque a opção 'continue' quebra a igualdade entre a lista de modos selecionada anteriormente
        # e a lista de modos do espaço de estados do MOB. Logo, esta lista irá propagar esta igualdade
        self.new_list = []
        
        
        space_all_modes = []
        #Este loop transforma cada modo selecinado no formato do espaço de
        # estados da funcao hyperopt. Entao, é passado para uma lista space_all_modes que, por sua vez,
        # eh passada para a funcao hp.choice. Isso evita a selecao de modos nao permitidos durante a otimizacao.        
        for mode in self.MOB.get_list_of_modes():          
            t_exp   = hp.uniform('t_exp_' + str(i), mode['min_t_exp'], mode['max_t_exp'])
            #t_exp   = hp.choice('t_exp_' + str(i), [0.00001])
            em_mode = hp.choice('em_mode_' + str(i), [mode['em_mode']])
            if mode['em_mode'] == 0:
                em_gain = hp.choice('em_gain_'+ str(i), [0]) #como o ganho nao tem influencia para em_mode=0, eu forco o zero.
            else:               
                max_em_gain = mode['em_gain']
                em_gain = hp.uniform('em_gain_'+ str(i), 2, max_em_gain)
                #em_gain = hp.choice('em_gain_'+ str(i), [2])                
            hss     = hp.choice('hss_' + str(i), [mode['hss']])
            preamp  = hp.choice('preamp_' + str(i),[mode['preamp']])
            binn    = hp.choice('binn_' + str(i), [mode['binn']])          
            sub_img = hp.choice('sub_img_' + str(i),[mode['sub_img']])              
            ccd_temp = hp.choice('ccd_temp_' + str(i),[self.ccd_temp])
            sky_flux = hp.choice('sky_flux_' + str(i), [self.sky_flux])
            star_flux = hp.choice('obj_flux_' + str(i), [self.star_flux])
            n_pix_star = hp.choice('n_pix_star_'+ str(i),[self.n_pix_star])
            serial_number = hp.choice('serial_number' + str(i), [self.serial_number])       
            new_mode = [t_exp, em_mode, em_gain, hss, preamp, binn, sub_img, ccd_temp, sky_flux, star_flux, n_pix_star, serial_number]            
            self.space_all_modes.append(new_mode)
            self.new_list.append(mode)
            #print(sample(new_mode))
            #print(max_em_gain*(sample(star_flux)/sample(n_pix_star)+sample(sky_flux))*mode['max_t_exp'])
            i+=1        
        self.space = hp.choice('operation_mode', self.space_all_modes)


    def run_bayesian_opt(self, max_evals):        
        # Create the algorithm
        tpe_algo = tpe.suggest

        # Create a trials object
        self.tpe_trials = Trials()
        
        #Parametros para normalizar a SNR e a FA
        mean_snr = np.mean(self.losses_SNR)                        
        mean_fa = np.mean(self.losses_FA)       
        #print(mean_snr, mean_fa), exit()        

        # Run evals with the tpe algorithm
        best_mode  = fmin(fn=function, space=self.space+[mean_snr, mean_fa, self.snr_target], algo=tpe_algo, trials=self.tpe_trials, max_evals=max_evals, rstate= np.random.RandomState(50))
        
        index_list_modes = best_mode['operation_mode']
        chosen_mode = self.new_list[index_list_modes]        

        t_exp = best_mode['t_exp_' + str(index_list_modes)]
        em_mode = chosen_mode['em_mode']
        #em_gain = sample(self.space_all_modes[int(index_list_modes)])[2]
        em_gain = best_mode['em_gain_' + str(index_list_modes)]
        hss = chosen_mode['hss']
        preamp = chosen_mode['preamp']
        binn = chosen_mode['binn']
        sub_img = chosen_mode['sub_img']
        self.best_mode = {'t_exp':t_exp, 'em_mode':em_mode, 'em_gain':em_gain,'hss':hss, 'preamp':preamp,'binn':binn, 'sub_img':sub_img, 'SNR*FA':-self.tpe_trials.best_trial['result']['loss']}
        
        #print(self.tpe_trials.idxs_vals[1])
        #print(self.best_mode)

        

    def run_bayesian_opt_2(self, max_evals):        
        # Create the algorithm
        tpe_algo = tpe.suggest

        # Create a trials object
        self.tpe_trials = Trials()
        
        #Parametros para normalizar a SNR e a FA
        mean_snr = np.mean(self.losses_SNR)
        std_snr = np.std(self.losses_SNR)        
        offset_snr = np.std(np.abs((np.asarray(self.losses_SNR)) - mean_snr)/std_snr)
        #offset_snr = 0
        mean_fa = np.mean(self.losses_FA)
        std_fa = np.std(self.losses_FA)
        offset_fa = np.std(np.abs((np.asarray(self.losses_FA)) - mean_fa)/std_fa)
        #offset_fa = 0
        
        #print(mean_snr, mean_fa), exit()        

        # Run evals with the tpe algorithm
        best_mode  = fmin(fn=function, space=self.space+[mean_snr, std_snr, mean_fa, std_fa, offset_snr, offset_fa, self.snr_target], algo=tpe_algo, trials=self.tpe_trials, max_evals=max_evals, rstate= np.random.RandomState(50))        

        index_list_modes = best_mode['operation_mode']
        chosen_mode = self.new_list[index_list_modes]   

        t_exp = best_mode['t_exp_' + str(index_list_modes)]
        em_mode = chosen_mode['em_mode']
        #em_gain = sample(self.space_all_modes[int(index_list_modes)])[2]
        em_gain = best_mode['em_gain_' + str(index_list_modes)]
        hss = chosen_mode['hss']
        preamp = chosen_mode['preamp']
        binn = chosen_mode['binn']
        sub_img = chosen_mode['sub_img']
        self.best_mode = {'t_exp':t_exp, 'em_mode':em_mode, 'em_gain':em_gain,'hss':hss, 'preamp':preamp,'binn':binn, 'sub_img':sub_img, 'SNR*FA':-self.tpe_trials.best_trial['result']['loss']}
        #print(self.tpe_trials.idxs_vals[1])
        #print(self.best_mode)
        
    

    def print_best_mode(self):                 
        if self.best_mode['em_mode'] == 1:
            print('\nEM Mode')
            print('-------')
            print('EM gain: ', self.best_mode['em_gain'])
        else:
            print('\nConventional Mode')
            print('-----------------')            
        print('Exposure time (s): ', self.best_mode['t_exp'])            
        print('HSS: ', self.best_mode['hss'])
        print('Preamp: ', self.best_mode['preamp'])
        print('Binning: ', self.best_mode['binn'])        
        print('Sub image: ', self.best_mode['sub_img'])
        print('\nBest SNR*FA: ', self.best_mode['SNR*FA'])       


    def creat_log_parameters(self, path):
        # neste loop eh criado um arquivo contendo o log dos parametros utilizados em cada iteração do MOB.
        # Esta função é necessária porque a biblioteca retorna apenas o indice da lista do modo utilizado. Este índice
        # é usado para obter os parâmetros "chutados" ao longo das iterações.
        # Os valores do EMGain e do t_exp precisam ser obtidos através do próprio LOG da biblioteca.                    
        opt_log = self.tpe_trials.idxs_vals[1]        
        op_modes_list = opt_log['operation_mode']

               
        # Este loop adiciona aos dicionários os valores chutados pelo MOB, separando-os por keywords. Estas keyword correspondem
        # ao índice do modo na lista de modos selecionados fornecida para o MOB.
        # Pode acontecer de uma keyword receber uma lista de valores. Este problema é resolvido com a função pop()
        # que retira sempre o primeiro valor da lista
        dic_em_gain = {}
        dic_t_exp = {}        
        for item, count in collections.Counter(op_modes_list).items():
           dic_em_gain[str(item)] = opt_log['em_gain_' + str(item)]
           dic_t_exp[str(item)] = opt_log['t_exp_' + str(item)]          

                
        array_dic_modes = []
        arq = open(path + 'log', 'w')
        for i in range(len(op_modes_list)):
            item = op_modes_list[i]
            snr_fa = -self.tpe_trials.results[i]['loss']            
            mode = self.new_list[item]
            t_exp = dic_t_exp[str(item)].pop(0)
            hss = mode['hss']
            em_mode = mode['em_mode']
            sub_img = mode['sub_img']
            binn = mode['binn']                            
            em_gain = dic_em_gain[str(item)].pop(0)
            preamp =  mode['preamp']
            dic = {'t_exp': t_exp, 'em_mode':int(em_mode), 'em_gain':int(em_gain), 'hss':int(hss), 'preamp':int(preamp), 'sub_img':int(sub_img), 'binn':int(binn), 'snr*fa':snr_fa}
            json.dump(dic, arq)
            arq.write('\n')
        arq.close()

        
       

    def creat_log_parameters_2(self):
        # neste loop eh criado um arquivo contendo o log dos parametros utilizados em cada itercao do MOB.
        # Esta função é necessária porque a biblioteca retorna apenas o número da iteração utilizada. Este número
        # é usado para obter os parâmetros "chutados" ao longo das iterações.
        # O valor do EMGain precisa ser obtido através do próprio LOG da biblioteca. Como podem ocorrer chutes repetidos,
        # este LOG armazena os valores do EMGAIN na mesma ordem em que foram utilizados. Dessa forma,
        # esta biblioteca "pinça" os valores de cada um destes parâmetros de acordo com as iterações.               
        opt_log = self.tpe_trials.idxs_vals[1]        
        op_modes_list = opt_log['operation_mode']

        
        # Estes dicionários recebem os valores do t_exp e em_gain na ordem em que foram escolhidos
        # Podem haver casos em que os valores recebidos são uma lista. Para tanto, o valor adequado da lista será
        # sempre o primeiro. Eu os retiro com a função pop()
        dic_em_gain = {}
        dic_t_exp = {}        
        for item, count in collections.Counter(op_modes_list).items():
           dic_em_gain[str(item)] = opt_log['em_gain_' + str(item)]            
           dic_t_exp[str(item)] = opt_log['t_exp_' + str(item)]

           
        arq = open(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\Graficos\Iteracoes_ruido_parametros\Logs\Parameters\log.txt', 'w')       
        for item in op_modes_list:
            s=''
            mode = self.new_list[item]
            t_exp = dic_t_exp[str(item)].pop(0)
            hss = mode['hss']
            em_mode = mode['em_mode']
            binn = mode['binn']
            sub_img = mode['sub_img']
            em_gain = dic_em_gain[str(item)].pop(0)
            #em_gain = sample(self.space_all_modes[item])[2]
            preamp =  mode['preamp']            
            s += str(t_exp) + '\t' + str(em_mode) + '\t' + str(em_gain) + '\t' + str(hss) + '\t' + str(preamp) + '\t' + str(binn) + '\t' + str(sub_img)            
            arq.write(s + '\n')                  
        arq.close()


    def creat_log_loss(self, path):           
        arq = open(path + 'log', 'w')        
        for x in self.tpe_trials.results:
            arq.write(str(-x['loss']))
            arq.write('\n')
        arq.write('Best SNR: %.2f'%(self.best_mode['SNR*FA']))
        arq.close()


    def export_optimal_setup(self, img_directory):
        dic={}        
        if self.best_mode['em_mode'] == 1:
            dic['em_mode'] = 'EM Mode'
            dic['em_gain'] = self.best_mode['em_gain']
        else:
            dic['em_mode'] = 'Conventional Mode'
        dic['t_exp'] = self.best_mode['t_exp']
        dic['hss'] = self.best_mode['hss']
        dic['preamp'] = self.best_mode['preamp']
        dic['bin'] = self.best_mode['binn']
        dic['sub_img'] = self.best_mode['sub_img']
        dic['SNR*FA'] = self.best_mode['SNR*FA']

        if img_directory!= '': os.chdir(img_directory)
        file_name = 'conv_'
        if self.best_mode['em_mode'] == 1: file_name='EM_'
        file_name+= str(self.best_mode['hss']) + 'MHz_' + 'PA' + str(self.best_mode['preamp']) + '_B' + str(self.best_mode['binn']) + '_SI' + str(self.best_mode['sub_img']) + '.txt'
        
        with open(file_name, 'w') as arq:
            json.dump(dic, arq, indent = 4, sort_keys=True)
            arq.close()
    
            

'''

    def SNR_FA_ranges_2(self):
        n = int(30/len(self.filtered_list))
        if n < 1:n=1
        
        vector_snr = []
        vector_fa = []
        for i in range(3):
            for mode in self.filtered_list:
                t_exp = rd.uniform(mode['min_t_exp'], mode['max_t_exp'])
                em_gain = rd.uniform(2, mode['em_gain'])
                
                parameters = [
                t_exp,
                mode['em_mode'],
                em_gain,
                mode['hss'],
                mode['preamp'],
                mode['binn'],
                mode['sub_img'],
                self.ccd_temp,
                self.sky_flux,
                self.star_flux,
                self.n_pix_star,
                self.serial_number,
                0, #mean_snr
                1, #std_snr 
                0, #mean_fa 
                1, #std_fa
                ]
                snr = function_snr(parameters)
                fa = function_fa(parameters)
                vector_snr.append(snr)       
                vector_fa.append(fa)

        #Parametros para normalizar a SNR e a FA
        self.mean_snr = np.mean(vector_snr)
        self.std_snr = np.std(vector_snr)
        self.mean_fa = np.mean(vector_fa)
        self.std_fa = np.std(vector_fa)
        #print(mean_snr, std_snr, mean_fa,std_fa )
'''

##    def create_list_of_modes(self):
##        list_all_modes_SNR, list_all_modes_FA = self.get_lists_of_modes()
##        for mode_snr in list_all_modes_SNR:
##            for mode_fa in list_all_modes_FA:
##                if mode_snr['em_mode'] == mode_fa['em_mode']:
##                    if mode_snr['hss'] == mode_fa['hss']:
##                        if mode_snr['binn'] == mode_fa['binn']:                            
##                            if mode_snr['t_exp'] < mode_fa['t_exp']:
##                                new_mode = copy(mode_snr)
##                                new_mode['sub_img'] = mode_fa['sub_img']                                
##                                new_mode['min_t_exp'] = new_mode['t_exp']
##                                new_mode['max_t_exp'] = mode_fa['t_exp']
##                                del new_mode['t_exp']
##                                self.filtered_list.append(new_mode)             



 #self.set_gain(mode['em_mode'], mode['hss'], mode['preamp'])                
                #max_em_gain = mode['em_gain']
                #if max_em_gain<2:
                #    print('Error: the required EM Gain is below 2x: %.2f'%(max_em_gain))
                #    continue                    
                #if max_em_gain>300:
                    #print('Warning: the required EM Gain is above 300x: %.2f'%(max_em_gain))
                #    max_em_gain = 300                    
                #em_gain     = hp.choice('em_gain_' + str(i), [2])
