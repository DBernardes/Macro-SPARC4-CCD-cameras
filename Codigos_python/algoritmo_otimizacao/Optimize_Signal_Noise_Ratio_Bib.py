#!/usr/bin/env python
# coding: utf-8

#Classe OptSNR criada para a otimizacao da relacao sinal-ruído da camera iXon Ultra
#888 atraves da biblioteca hyperopt. Sera usada a classe SNRCalc
#para fornecer o valor do SNR para cada modo
#de operacao da camera avaliado.
#Denis Varise Bernardes.
#12/12/2019.


import SNR_Calculation_Bib as SNRCB
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Modos_Operacao_Bib as MOB
import collections
import os, json
from sys import exit
from hyperopt import hp, tpe, rand, Trials, fmin
from hyperopt.pyll.stochastic import sample
from hyperopt.pyll import scope
from copy import copy



def function(parameters):   
    t_exp = parameters[0]
    em_mode = parameters[1]
    em_gain = parameters[2]
    hss = parameters[3]
    preamp = parameters[4]
    binn = parameters[5]    
    ccd_temp = parameters[6]
    sky_flux = parameters[7]
    star_flux = parameters[8]
    n_pix_star = parameters[9]
    serial_number = parameters[10]
    snr_target = parameters[11]
    SNRC = SNRCB.SignalToNoiseRatioCalc(t_exp = t_exp,
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
    if snr < snr_target: snr=0
    return -snr


#-------------------------------------------------------------------

class OptSignalNoiseRation:

    def __init__(self, snr_target, serial_number, ccd_temp, n_pix_star, sky_flux, star_flux):        
        self.MOB = MOB.ModosOperacao()
        self.space = []
        self.best_mode = {}        
        self.list_all_modes  = []
        self.filtered_list = [] #esta lista foi criada para filtrar os modos repetidos da list_all_modes
        self.best_sub_img = []
        self.new_list = []

        self.hss = [[],[]]
        self.binn = [[],[]]
        self.sub_img = []
        #self.t_exp = t_exp
        self.ccd_temp = ccd_temp
        self.serial_number = serial_number
        self.gain = 0 #preamp gain
        self.dark_noise = 0
        self.set_dc() #função para setar a corrente de escuro
        self.snr_target = snr_target #esta é a snr desejada      
        
        self.sky_flux = sky_flux #e-/pix/s                
        self.star_flux = star_flux #e-/s        
        self.n_pix_star = n_pix_star
       
        
    def write_mode_to_MOB_class(self, em_mode, em_gain, hss, preamp, binn, sub_img, t_exp):
        #Escreve os modos selecinados em uma lista de dicionarios
        self.MOB.write_mode(em_mode, em_gain, hss, preamp, binn, sub_img, t_exp)

   
    def print_MOB_list(self):        
        lista = self.MOB.get_list_of_modes()
        for modo in lista:
            print(modo)

    def write_MOB_obj(self, obj):
        self.MOB = obj

    def read_MOB_obj(self):
        return self.MOB


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


    def calc_max_em_gain(self, t_exp):
        #Cálculo do ganho EM máximo permitido para cada modo. O cálculo é baseado na quantidade máxima de 100 fótons
        # por pixel do CCD para a qual o modo EM é melhor que o Convencional.
        # Esta função recebe o t_exp máximo de cada modo. Contudo, dentro de um mesmo modo, o ganho EM poderia ser maior
        # quando a iteração escolher um t_exp menor. Talvez, esta seja uma limitação da biblioteca. Ainda não achei solução        
        max_fotons = 100
        bias = 500
        max_ADU = (2**16)*0.8
        #print(self.sky_flux, self.star_flux, self.n_pix_star, self.dark_noise,t_exp)  
        aux = (self.sky_flux + self.star_flux/self.n_pix_star + self.dark_noise)*t_exp        
        max_em_gain = max_ADU/(aux/self.gain+bias)        
        if aux > max_fotons:
            max_em_gain = 0                   
        
        return max_em_gain



    def calc_max_em_gain_2(self, t_exp):
        #Cálculo do ganho EM máximo permitido para cada modo. O cálculo é baseado na quantidade máxima de 100 fótons
        # por pixel do CCD para a qual o modo EM pe melhor que o Convencional.
        # Esta função recebe o t_exp máximo de cada modo. Contudo, dentro de um mesmo modo, o ganho EM poderia ser maior
        # quando a iteração escolher um t_exp menor. Talvez, esta seja uma limitação da biblioteca. Ainda não achei solução
        max_fotons = 100               
        aux = (self.sky_flux + self.star_flux/self.n_pix_star + self.dark_noise)*t_exp        
        max_em_gain = max_fotons/aux #Este é o ganho EM para que o fluxo de fótons seja igual a 100, para um t_exp máximo        
        return max_em_gain


        

    # Esta função determina os modos de operação que atendem a uma SNR mínima
    # Para cada modo de operação é calculado o em_gain máximo. Este ganho é utilizado para
    # calcular qual o texp mínimo permitido para atingir o SNR. Os modos selecionados são passados para
    # a lista de modos do objeto MOB 
    def determine_operation_modes_minimun_SNR(self):                   
        for mode in self.MOB.get_list_of_modes():            
            em_mode = mode['em_mode']
            hss = mode['hss']
            binn = mode['binn']
            max_t_exp = mode['max_t_exp']
            sub_img = mode['sub_img']
            for preamp in [1,2]:
                if em_mode == 0:
                    max_em_gain = 0
                else:
                    self.set_gain(em_mode, hss, preamp)                    
                    max_em_gain = self.calc_max_em_gain(max_t_exp)
                    if max_em_gain<2:
                        print('The EM Gain required for this mode is below 2x: %.2f'%(max_em_gain))
                        continue #este continue quebra a iteração do laço, ou seja, o modo avaliado não é adicionado               
                    if max_em_gain>300:                                
                        max_em_gain = 300                
                SNRC = SNRCB.SignalToNoiseRatioCalc(max_t_exp, em_mode, max_em_gain, hss, preamp, binn, self.ccd_temp, self.sky_flux, self.star_flux, self.n_pix_star, self.serial_number)
                SNRC.set_gain_value()
                SNRC.calc_RN()
                SNRC.calc_DC()                
                min_t_exp = SNRC.calc_minimun_texp_provided_SNR(self.snr_target)                
                if min_t_exp <= max_t_exp:
                    dic = {'em_mode':em_mode, 'em_gain':max_em_gain, 'hss':hss, 'preamp':preamp, 'binn':binn, 'sub_img':sub_img, 'min_t_exp':min_t_exp, 'max_t_exp':max_t_exp}                    
                    self.filtered_list.append(dic)         
        self.MOB.write_list_of_modes(self.filtered_list)
        



    def duplicate_list_of_modes_for_PA12(self):
        self.list_all_modes = self.MOB.get_list_of_modes() #Cria uma lista dos modos permitidos        
        
        #Nesta etapa, são descartados os modos sub_img repetidos. Contudo, ainda é
        # necessário filtrar os modos com texp máximo sobrepostos.
        
        #Cada iteração recebe um dos valores de preamp: 1 ou 2. Preciso saber o valor do preamp de forma antecipada
        #para calcular o valor máximo do EMGAIN

        #Precisei colocar esta função para fora do create_space porque os modos de otimização 2 e 3 tratam a lista
        # de modos selecionados de forma diferente
        
        for preamp in [1,2]: 
            for mode in self.list_all_modes:
                new_mode = {'em_mode':mode['em_mode'], 'hss':mode['hss'], 'preamp':preamp, 'binn':mode['binn'], 'max_t_exp':mode['max_t_exp'], 'min_t_exp':mode['min_t_exp']}
                if new_mode not in self.filtered_list: self.filtered_list.append(new_mode)
        
        #for mode in self.filtered_list:print(mode)

                

    def create_space(self):
        #Esta estrutura de ifs é necessária para eliminar modos repetidos, porém, com diferentes tempos máximos de exposição
        # resultantes de modos com sub_imgs diferentes. Após a execução do MOB, o modo sub_img é selecionado para o maior
        # valor cujo o t_exp esteja dentro do limite máximo permitido para aquele modo.
        new_list = []
        for i in range(len(self.filtered_list)-1):          
            mode_before = self.filtered_list[i]            
            mode_after = self.filtered_list[i+1]           
            if (mode_before['em_mode'] == mode_after['em_mode']):
                if(mode_before['hss'] == mode_after['hss']):
                    if (mode_before['binn'] == mode_after['binn']):
                        if(mode_before['preamp'] == mode_after['preamp']):
                            if (mode_before['max_t_exp'] < mode_after['max_t_exp']):
                                new_list.append(mode_before)
        for mode in new_list:
            self.filtered_list.remove(mode)

        #for mode in self.filtered_list:print(mode)
                
        i=0
        space_all_modes = []
        
        #Fiz esta lista porque a opção 'continue' quebra a igualdade entre a lista de modos selecionada anteriormente
        # e a lista de modos do espaço de estados do MOB. Logo, usa esta lista para recuperar os modos iterados pelo MOB    
        self.new_list = []     
        
        #Este loop transforma cada modo selecinado pelo optimize_acquisition_rate no formato do espaço de
        # estados da funcao hyperopt. Cada modo é, então, passado para a lista space_all_modes que, por sua vez,
        # é passada para a funcao hp.choice. Isso evita a selecao de modos nao permitidos durante a otimizacao.        
        for mode in self.filtered_list:
            t_exp   = hp.uniform('t_exp_' + str(i), mode['min_t_exp'], mode['max_t_exp'])
            #t_exp   = hp.choice('t_exp_' + str(i), [0.00001])
            em_mode = hp.choice('em_mode_' + str(i), [mode['em_mode']])
            if mode['em_mode'] == 0:
                em_gain = hp.choice('em_gain_'+ str(i), [0]) #como o ganho nao tem influencia para em_mode=0, eu forço o zero.
            else:
                self.set_gain(mode['em_mode'], mode['hss'], mode['preamp'])                
                max_em_gain = self.calc_max_em_gain(mode['max_t_exp'])                
                if max_em_gain<2:
                    print('The required EM Gain for this mode is below 2x: %.2f'%(max_em_gain))                    
                    continue
                if max_em_gain>300:                    
                    max_em_gain = 300
                #em_gain = hp.choice('em_gain_'+ str(i), [2])
                em_gain = hp.uniform('em_gain_'+ str(i), 2, max_em_gain)
            hss     = hp.choice('hss_' + str(i), [mode['hss']])
            preamp  = hp.choice('preamp_' + str(i),[mode['preamp']])       
            binn    = hp.choice('binn_' + str(i), [mode['binn']])            
            ccd_temp = hp.choice('ccd_temp_' + str(i),[self.ccd_temp])
            sky_flux = hp.choice('sky_flux_' + str(i), [self.sky_flux])
            star_flux = hp.choice('obj_flux_' + str(i), [self.star_flux])
            n_pix_star = hp.choice('n_pix_star_'+ str(i),[self.n_pix_star])
            serial_number = hp.choice('serial_number' + str(i), [self.serial_number])       
            new_mode = [t_exp, em_mode, em_gain, hss, preamp, binn, ccd_temp, sky_flux, star_flux, n_pix_star, serial_number]
            self.new_list.append(mode)
            #print(sample(new_mode))
            space_all_modes.append(new_mode)
            i+=1        
        self.space = hp.choice('operation_mode', space_all_modes)
        

    def print_filtered_list_of_modes(self):
        for mode in self.filtered_list:
            print(mode)
      

    def run_bayesian_opt(self, max_evals, algorithm = tpe.suggest):
        # Create the algorithm
        algo = algorithm

        # Create a trials object
        self.tpe_trials = Trials()       
        

        # Run evals with the tpe algorithm
        best_mode  = fmin(fn=function, space=self.space+[self.snr_target], algo=algo, trials=self.tpe_trials, max_evals=max_evals, rstate= np.random.RandomState(50))
        
        index_list_modes = best_mode['operation_mode']
        chosen_mode = self.new_list[index_list_modes]        
        t_exp = best_mode['t_exp_' + str(index_list_modes)]
        em_mode = chosen_mode['em_mode']
        em_gain = best_mode['em_gain_' + str(index_list_modes)]
        hss = chosen_mode['hss']
        preamp = chosen_mode['preamp']
        binn = chosen_mode['binn']
        self.best_mode = {'t_exp':t_exp, 'em_mode':em_mode, 'em_gain':em_gain,'hss':hss, 'preamp':preamp,'binn':binn, 'SNR':-self.tpe_trials.best_trial['result']['loss']}        
        #print(self.tpe_trials.idxs_vals[1])


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
        arq = open(path + 'log.txt', 'w')
        for i in range(len(op_modes_list)):
            item = op_modes_list[i]
            snr = -self.tpe_trials.results[i]['loss']            
            mode = self.new_list[item]
            t_exp = dic_t_exp[str(item)].pop(0)
            hss = mode['hss']
            em_mode = mode['em_mode']
            binn = mode['binn']                            
            em_gain = dic_em_gain[str(item)].pop(0)
            preamp =  mode['preamp']
            dic = {'t_exp': t_exp, 'em_mode':int(em_mode), 'em_gain': int(em_gain), 'hss':int(hss), 'preamp':int(preamp), 'binn':int(binn), 'snr':snr}            
            #array_dic_modes.append(dic)            
            json.dump(dic, arq)
            arq.write('\n')            
        arq.close()            
        
            

    def creat_log_loss(self, path):           
        arq = open(path + 'log.txt', 'w')        
        for x in self.tpe_trials.results:
            arq.write(str(-x['loss']))
            arq.write('\n')
        arq.write('Best SNR: %.2f'%(self.best_mode['SNR']))
        arq.close()


    def creat_log_parameters_3(self):
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
           
        arq = open(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\Graficos\Iteracoes_ruido_parametros\Logs\Parameters\log.txt', 'w')       
        for item in op_modes_list:            
            s=''
            mode = self.new_list[item]
            t_exp = dic_t_exp[str(item)].pop(0)
            hss = mode['hss']
            em_mode = mode['em_mode']
            binn = mode['binn']                            
            em_gain = dic_em_gain[str(item)].pop(0)
            preamp =  mode['preamp']            
            s += str(t_exp) + '\t' + str(em_mode) + '\t' + str(em_gain) + '\t' + str(hss) + '\t' + str(preamp) + '\t' + str(binn)
            arq.write(s + '\n')                  
        arq.close()
        

        


    def creat_log_parameters_2(self):
        # neste loop eh criado um arquivo contendo o log dos parametros utilizados em cada itercao do MOB.
        # Esta função é necessária por causa da forma como a biblioteca retorna os valores.
        # Como podem haver valores repetidos, a lista dos valores utilizados precisa ser dividida entre
        # os casos que aparecem uma unica vez e aqueles que aparecem duas ou mais. Os casos que aparecem
        # duas ou mais vezes precisam passar por um novo loop para separar cada modo utilizado
        opt_log = self.tpe_trials.idxs_vals[1]
        op_modes_list = opt_log['operation_mode']
        arq = open(r'C:\Users\denis\Desktop\UNIFEI\Projeto_Mestrado\Codigos\Graficos\Iteracoes_ruido_parametros\Logs\Loss\log.txt', 'w')
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


 

    def find_sub_img_best_mode(self):        
        for mode in self.list_all_modes:       
            if mode['em_mode'] == self.best_mode['em_mode']:
                if mode['hss'] == self.best_mode['hss']:
                    if mode['binn'] == self.best_mode['binn']:
                        #Este if foi colocado porque podem haver casos onde o modo ótimo possui varios sub-imgs,
                        # contudo, o t_exp que otimiza o SNR pode exceder o t_exp maximo para algum sub-img,
                        # prejudicando a FA. Portanto, este if seleciona apenas os sub-imgs que atendem ao
                        # requisito do t_exp máximo.
                        if self.best_mode['t_exp'] <= mode['max_t_exp']:
                            self.best_sub_img.append(mode['sub_img'])
            
        
    

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
        print('Sub image: ', max(self.best_sub_img))
        print('\nBest SNR: ', self.best_mode['SNR'])
        if self.snr_target > self.best_mode['SNR']: print('\nIt was not possible to reach the provided SNR.')


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
        dic['sub_img'] = max(self.best_sub_img)
        dic['SNR'] = self.best_mode['SNR']

        if img_directory!= '': os.chdir(img_directory)
        file_name = 'conv_'
        if self.best_mode['em_mode'] == 1: file_name='EM_'
        file_name+= str(self.best_mode['hss']) + 'MHz_' + 'PA' + str(self.best_mode['preamp']) + '_B' + str(self.best_mode['binn']) + '_SI' + str(max(self.best_sub_img)) + '.txt'
        
        with open(file_name, 'w') as arq:
            json.dump(dic, arq, indent = 4, sort_keys=True)
            arq.close()


    def export_optimal_setup_2(self, img_directory):
        string = ''
        if self.best_mode['em_mode'] == 1:
            string+='''EM Mode
-------
EM gain: '''+str(self.best_mode['em_gain'])
        else:
            string+='''Conventional Mode
-----------------            
Exposure time (s): '''+str(self.best_mode['t_exp'])
        string+='\nHSS: '+ str(self.best_mode['hss'])
        string+='\nPreamp: '+ str(self.best_mode['preamp'])
        string+='\nBinning: '+ str(self.best_mode['binn'])
        string+='\nSub image: '+ str(max(self.best_sub_img))
        string+='\nBest SNR: '+ str(self.best_mode['SNR'])

        if img_directory!= '': os.chdir(img_directory)
        file_name = 'conv_'
        if self.best_mode['em_mode'] == 1: file_name='EM_'
        file_name+= str(self.best_mode['hss']) + 'MHz_' + 'PA' + str(self.best_mode['preamp']) + '_B' + str(self.best_mode['binn']) + '_SI' + str(max(self.best_sub_img)) + '.txt'
        
        with open(file_name, 'w') as arq:
            arq.write(string)
            arq.close()
        

        
