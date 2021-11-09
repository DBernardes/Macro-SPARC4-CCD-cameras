#!/usr/bin/env python
# coding: utf-8

# Esta biblioteca gerencia o processo de otimização dos modos de
# operação dos CCDs. 

#10/01/2020. Denis Varise Bernardes.

import Optimize_Signal_Noise_Ratio_Bib as osnr
import Optimize_Acquisition_Rate_Bib as oar
import Optimize_Signal_Noise_Ratio_and_Acquisition_Rate_Bib as osnrar
import Photon_Flux_Calc_Bib as pfc
from sys import exit
from useful_functions import get_obs_setup
import os




class Optimize_Operation_Mode:

    def __init__(self, img_dir):
        snr, acq_rate, obj_magnitude, sub_img_modes, binn_modes, serial_number, ccd_temp, max_evals, export_arq, use_pre_img, pre_img_name, obj_coords, bias_img_name, sky_radius = get_obs_setup(img_dir)
        #print(snr, acq_rate, obj_magnitude, sub_img_modes, binn_modes, serial_number, ccd_temp, n_pix_star, max_evals)
        self.snr = snr
        self.acq_rate = acq_rate
        self.obj_magnitude = obj_magnitude
        self.max_evals = max_evals
        self.export_arq = export_arq
        
        self.sub_img_modes = sub_img_modes
        self.binn_modes = binn_modes
        self.serial_number = serial_number
        self.ccd_temp = ccd_temp        
        
        self.sky_flux = 12.298897076737294 #e-/pix/s
        self.hats24_flux = 56122.295000000006 #e-/s
        self.star_flux = 0
        self.n_pix_star = 305
        self.hats24_magnitude = 12.8
        
        self.use_pre_img = use_pre_img
        self.img_directory = img_dir+ '\\'
        self.pre_img_name = pre_img_name
        self.obj_coords = obj_coords
        self.bias_img_name = bias_img_name 
        self.sky_radius = sky_radius

        #os.chdir(img_directory) #muda para o diretório das imagens
        

    def verify_provides_modes(self):
        for sub_img in self.sub_img_modes:
            if sub_img not in [1024,512,256]:
                print('\nModo sub-image inválido! [%i]'%sub_img)
                #print(sub_img)
                exit()
        for binn in self.binn_modes:
            if binn not in [1,2]:
                print('\nModo binning inválido! [%i]'%binn)
                #print(binn)
                exit()

    def calc_star_flux(self):
        if self.use_pre_img == 's': self.calc_star_sky_flux_from_preimg()
        if self.use_pre_img == 'n': self.calc_star_sky_flux_from_magnitude()        

    def calc_star_sky_flux_from_preimg(self):
        #Inicia o objeto para a redução da pré-imagem
        pre_img_name = self.img_directory + self.pre_img_name
        bias_img_name = self.img_directory + self.bias_img_name        
        PFC = pfc.PhotonFluxCalc(img_name = pre_img_name, bias_name = bias_img_name, xy_star = self.obj_coords , sky_radius = self.sky_radius, ccd_serial=self.serial_number)
        #Lê a imagem de bias fornecida
        PFC.read_bias_img()
        #Calcula o fluxo do céu e da estrela para um raio ótimo
        PFC.calc_star_sky_flux()
        dc, rn, snr, sky_flux, sky_var, star_flux, star_var, n_pix_star, star_radius = PFC.get_results()        
        self.sky_flux = sky_flux
        self.star_flux = star_flux
        self.n_pix_star = n_pix_star
##        print(self.star_flux)
##        print(star_radius)
##        exit()


    def calc_star_sky_flux_from_magnitude(self):
        #Com base na magnitude fornecido pelo usuário, é calculado o fluxo de fótons do objeto
        # em relação do fluxo do hats24.
        aux = 10**((self.hats24_magnitude - self.obj_magnitude)/2.5)
        self.star_flux = self.hats24_flux*aux
        #print(self.star_flux),exit()


    def optimize(self, fixar_param):
        if fixar_param == 1: self.Optimize_SNR_provided_FA()
        if fixar_param == 2: self.Optimize_FA_provided_SNR()
        if fixar_param == 3: self.Optimize_SNR_and_AR()

    def Optimize_SNR_provided_FA(self):
        # Inicializa o objeto para a determinacao da frequencia de aquisicao
        OAR =  oar.OptimizeAcquisitionRate(acquisition_rate = self.acq_rate,
                                           sub_img_modes=self.sub_img_modes,
                                           binn_modes=self.binn_modes)       
        #Determina quais modos se encaixam nos parametros passados
        OAR.determine_operation_modes()
        #Retorna um objeto contendo os modos de operacao selecionados
        obj_lista_modos = OAR.read_MOB_obj()
        #Cria a lista de modos à partir do objeto MOB        
        #OAR.print_MOB_list(), exit()
        
        #cria o objeto da classe que executa o metodo de otimizacao
        OSNR = osnr.OptSignalNoiseRation(snr_target = self.snr,
                                         serial_number = self.serial_number,
                                         ccd_temp = self.ccd_temp,
                                         n_pix_star = self.n_pix_star,
                                         sky_flux = self.sky_flux,
                                         star_flux = self.star_flux)

        #escreve na classe a lista dos modos que atendem ao requisito da Freq.
        OSNR.write_MOB_obj(obj_lista_modos)       
        #imprime na tela os modos de operação selecionados pela biblioteca acquisition_frequency
        #OSNR.print_MOB_list(),exit()
        #duplica a lista dos modos selecionados para preamp 1 e 2
        OSNR.duplicate_list_of_modes_for_PA12()        
        #cria o dominio da funcao de interesse
        OSNR.create_space()
        #imprime a lista filtrada dos modos de operação. Não deve aparecer modo redundante para o caso do SNR
        #OSNR.print_filtered_list_of_modes()
        #executa o metodo de otimizacao bayesiano
        OSNR.run_bayesian_opt(max_evals=self.max_evals)
        #cria um arquivo contendo o log dos valores do ruido obtidos em cada iteracao
        #OSNR.creat_log_loss()
        #cria um arquivo contendo o log dos parametros utilizados em cada iteracao
        OSNR.creat_log_parameters(self.img_directory)
        #encontra o maior sub_img para o modo selecionado
        OSNR.find_sub_img_best_mode()
        #printa na tela o melhor modo
        OSNR.print_best_mode()
        
        if 's' in self.export_arq:
           OSNR.export_optimal_setup(self.img_directory)



    def Optimize_FA_provided_SNR(self):
        # Inicializa o objeto para a determinacao da frequencia de aquisicao ótima
        OAR =  oar.OptimizeAcquisitionRate(acquisition_rate = self.acq_rate,
                                           sub_img_modes=self.sub_img_modes,
                                           binn_modes=self.binn_modes)
        
        #Determina quais modos se encaixam nos parametros passados (bin e sub-img)
        OAR.determine_operation_modes()
        #Retorna um objeto contendo os modos de operacao selecionados
        obj_lista_modos_FA = OAR.read_MOB_obj()
        #Cria a lista de modos à partir do objeto MOB        
        #OAR.print_MOB_list()        
        
        #----------------------------------------------------------------------------
        #Faço essa inverção porque preciso o texp máximo de cada modo que atinge a FA
        #mínima. Com base nisso, calculo o valor do ganho EM máximo correspondente.         
        
        #cria o objeto da classe que encontra os modos de SNR permitidos
        OSNR = osnr.OptSignalNoiseRation(serial_number = self.serial_number,
                                         snr_target = self.snr,
                                         ccd_temp = self.ccd_temp,
                                         n_pix_star = self.n_pix_star,
                                         sky_flux = self.sky_flux,
                                         star_flux = self.star_flux)
        #escreve na classe a lista dos modos que atendem ao requisito da Freq.
        OSNR.write_MOB_obj(obj_lista_modos_FA)
        #OAR.print_MOB_list(),exit()
        # determina os modos de operação que atendem ao SNR mínimo fornecido
        OSNR.determine_operation_modes_minimun_SNR()                                                   
        # Lê o objeto Modos de Operação contendo a lista dos modos selecionados
        obj_list_of_modes = OSNR.read_MOB_obj()      
        # Imprime a lista de objetos na tela
        #OSNR.print_MOB_list(),exit()
        #----------------------------------------------------------------------------


        list_of_modes = [        
        {'em_mode': 1, 'em_gain': 2, 'hss': 10, 'preamp': 1, 'binn': 1, 'sub_img': 512, 'min_t_exp': 0.03, 'max_t_exp': 15},
        {'em_mode': 1, 'em_gain': 2, 'hss': 10, 'preamp': 1, 'binn': 1, 'sub_img': 256, 'min_t_exp': 0.03, 'max_t_exp': 15}        
        ]    
        #obj_list_of_modes.write_list_of_modes(list_of_modes)

        
        # Escreve dentro da classe o objeto contendo os modos de operação selecionados pela OSNR
        OAR.write_MOB_obj(obj_list_of_modes)       
        #Imprime na tela os modos de operação fornecidos
        #OAR.print_MOB_list(),exit()
        #Determina o modo de operação mais rápido contido na lista do objeto MOB
        OAR.determine_fastest_operation_mode()
        #Imprime na tela o melhor modo
        OAR.print_best_mode()

        if 's' in self.export_arq:
           OAR.export_optimal_setup(self.img_directory)
       

    def Optimize_SNR_and_AR(self):
        # Inicializa o objeto para a determinacao da frequencia de aquisicao
        OAR =  oar.OptimizeAcquisitionRate(acquisition_rate = self.acq_rate, sub_img_modes=self.sub_img_modes, binn_modes=self.binn_modes)    
        #Determina quais modos se encaixam nos parametros passados
        OAR.determine_operation_modes()
        #Retorna um objeto contendo os modos de operacao selecionados
        obj_lista_modos_FA = OAR.read_MOB_obj()
        #Cria a lista de modos à partir do objeto MOB        
        #OAR.print_MOB_list(),exit()
           
        

        #cria o objeto da classe que encontra os modos de SNR permitidos
        OSNR = osnr.OptSignalNoiseRation(serial_number = self.serial_number,
                                         snr_target = self.snr,
                                         ccd_temp = self.ccd_temp,
                                         n_pix_star = self.n_pix_star,
                                         sky_flux = self.sky_flux,
                                         star_flux = self.star_flux)
        #escreve na classe a lista dos modos que atendem ao requisito da Freq.
        OSNR.write_MOB_obj(obj_lista_modos_FA)        
        #OSNR.print_MOB_list(),exit()
        # determina os modos de operação que atendem ao SNR mínimo fornecido
        OSNR.determine_operation_modes_minimun_SNR()        
        # Lê o objeto Modos de Operação contendo a lista dos modos selecionados
        obj_list_of_modes = OSNR.read_MOB_obj()       
        # Imprime a lista de objetos na tela
        #OSNR.print_MOB_list(),exit()
        
        
        #Cria o objeto que otimiza a SNR e a FA ao mesmo tempo
        OSNRAR = osnrar.Opt_SignalNoiseRatio_AcquisitionRate(snr_target = self.snr,
                                                           acq_rate = self.acq_rate,
                                                           sub_img_modes = self.sub_img_modes,
                                                           binn_modes = self.binn_modes,
                                                           serial_number = self.serial_number,
                                                           ccd_temp = self.ccd_temp,
                                                           n_pix_star = self.n_pix_star,
                                                           sky_flux = self.sky_flux,
                                                           star_flux = self.star_flux)
        

        
        list_of_modes = [        
        {'em_mode': 1, 'em_gain': 2, 'hss':  1, 'preamp': 1, 'binn': 1, 'sub_img': 1024, 'min_t_exp': 0.00001, 'max_t_exp': 1},
        {'em_mode': 1, 'em_gain': 2, 'hss': 10, 'preamp': 1, 'binn': 1, 'sub_img': 1024, 'min_t_exp': 0.00001, 'max_t_exp': 1},
        {'em_mode': 1, 'em_gain': 2, 'hss': 20, 'preamp': 1, 'binn': 1, 'sub_img': 1024, 'min_t_exp': 0.00001, 'max_t_exp': 1},
        {'em_mode': 1, 'em_gain': 2, 'hss': 30, 'preamp': 1, 'binn': 1, 'sub_img': 1024, 'min_t_exp': 0.00001, 'max_t_exp': 1},
            
        ]    
        #obj_list_of_modes.write_list_of_modes(list_of_modes)

        #Escreve na classe o obj com a lista de modos selecionados pela FA e SNR
        OSNRAR. write_MOB_obj(obj_list_of_modes)
        #OSNRAR.print_MOB_list(),exit()
        # Realiza várias iterações para o cálculo da média e desvio padrão da SNR e FA
        # Possui um problema. A SNR pode não ser atingida caso o texp e o em_gain escolhidos
        # sejam muito pequenos. Quando isso ocorre, a função retorna valor zero (descarta)
        OSNRAR.SNR_FA_ranges()
        #Cria o espaço de estados no formato do MOB.
        OSNRAR.create_space()       
        # Roda o MOB para a quantidade de iterações fornecida
        OSNRAR.run_bayesian_opt(max_evals=self.max_evals)
        #printa na tela o melhor modo
        OSNRAR.print_best_mode()
        #cria um arquivo contendo o log dos valores do ruido obtidos em cada iteracao
        #OSNRAR.creat_log_loss()
        #cria um arquivo contendo o log dos parametros utilizados em cada iteracao
        OSNRAR.creat_log_parameters(self.img_directory)
        
        if 's' in self.export_arq:
           OSNRAR.export_optimal_setup(self.img_directory)



           
