#!/usr/bin/env python
# coding: utf-8

#Este codigo cotem a classe AcquisitionRateCalc que calcula
#o valor da frequencia de aquisicao para a camera CCD iXon Ultra EMCCD
#em funcao do modo de operacao. O calculo e realizado
#com base nos dados das caracterizacoes da camera e estruturados
#em planilhas excel.
#Denis Varise Bernardes.
#08/10/2019.

from scipy.interpolate import interp1d
import pandas as pd
import math
import numpy as np
from sys import exit

class AcquisitionRateCalc:

    def __init__(self):        
        self.acquisition_rate = 0
        self.t_corte = 0
        self.tab_valores_readout = 'planilhas/Tabela_Valores_Readout.xlsm'
        self.max_t_exp = 0


    def write_operation_mode(self, em_mode, hss, binn, sub_img, t_exp):
        self.t_exp = t_exp
        self.em_mode = em_mode        
        self.hss = hss        
        self.binn = binn
        self.sub_img = sub_img        

    def read_tab_return_column(self, tab_name, column_name):
        df = pd.read_excel(tab_name) 
        columns = pd.DataFrame(df)
        return columns[column_name]


    def define_acq_rate_tab_name(self):
        #monta a string do nome da planilha em funcao do modo de operacao do CCD
        tab_name = 'X' + str(self.sub_img) + 'B' + str(self.binn) + 'HSS'
        if self.hss == 0.1:
            tab_name+= '01'
        else:
            tab_name+= str(self.hss)
        return 'planilhas/' + tab_name + '.xlsm'


    def calc_acquisition_rate_texp_greater_tcorte(self):
        self.acquisition_rate = 1/self.t_exp       
        

    def calc_acquisition_rate_texp_lower_tcorte(self):
        #nome da planilha com a curva de acq_rate x t_exp
        tab_name = self.define_acq_rate_tab_name()
        #retorna a coluna com o tempo de exposicao
        t_exp_column = self.read_tab_return_column(tab_name, 'TEXP (s)')
        t_exp_column = self.filter_list(t_exp_column)
        #retorna a coluna com a frequencia de aquisicao
        acq_rate_column = self.read_tab_return_column(tab_name, 'FREQ (fps)')
        acq_rate_column = self.filter_list(acq_rate_column)
        #print(t_exp_column,acq_rate_column) 
        #interpola os dados        
        f = interp1d(t_exp_column, acq_rate_column)
        #calcula a frequencia de aquisicao com base na interpolacao
        self.acquisition_rate = f(self.t_exp) 


    def filter_list(self, lista):
        for i in range(len(lista)):        
            if math.isnan(lista[i]):
                lista = lista[0:i]
                break
            else:
                pass       
        return lista


    def seleciona_t_corte(self):
        #Os ifs verificam se o t_exp esta antes ou depois do t_c
        # em funcao do modo de operacao
        indice_tab_t_corte = 0
        if self.hss == 30:
            if self.sub_img == 1024:
                if self.binn == 2:
                    indice_tab_t_corte = 1
                if self.binn == 1:
                    indice_tab_t_corte = 2
            if self.sub_img == 512:
                if self.binn == 2:
                    indice_tab_t_corte = 3
                if self.binn == 1:
                    indice_tab_t_corte = 4
            if self.sub_img == 256:
                if self.binn == 2:
                    indice_tab_t_corte = 5
                if self.binn == 1:
                    indice_tab_t_corte = 6
        if self.hss == 20:
            if self.sub_img == 1024:
                if self.binn == 2:
                    indice_tab_t_corte = 7
                if self.binn == 1:
                    indice_tab_t_corte = 8
            if self.sub_img == 512:
                if self.binn == 2:
                    indice_tab_t_corte = 9
                if self.binn == 1:
                    indice_tab_t_corte = 10
            if self.sub_img == 256:
                if self.binn == 2:
                    indice_tab_t_corte = 11
                if self.binn == 1:
                    indice_tab_t_corte = 12
        if self.hss == 10:
            if self.sub_img == 1024:
                if self.binn == 2:
                    indice_tab_t_corte = 13
                if self.binn == 1:
                    indice_tab_t_corte = 14
            if self.sub_img == 512:
                if self.binn == 2:
                    indice_tab_t_corte = 15
                if self.binn == 1:
                    indice_tab_t_corte = 16
            if self.sub_img == 256:
                if self.binn == 2:
                    indice_tab_t_corte = 17
                if self.binn == 1:
                    indice_tab_t_corte = 18
        if self.hss == 1:
            if self.sub_img == 1024:
                if self.binn == 2:
                    indice_tab_t_corte = 19
                if self.binn == 1:
                    indice_tab_t_corte = 20
            if self.sub_img == 512:
                if self.binn == 2:
                    indice_tab_t_corte = 21
                if self.binn == 1:
                    indice_tab_t_corte = 22
            if self.sub_img == 256:
                if self.binn == 2:
                    indice_tab_t_corte = 23
                if self.binn == 1:
                    indice_tab_t_corte = 24
        if self.hss == 0.1:
            if self.sub_img == 1024:
                if self.binn == 2:
                    indice_tab_t_corte = 25
                if self.binn == 1:
                    indice_tab_t_corte = 26
            if self.sub_img == 512:
                if self.binn == 2:
                    indice_tab_t_corte = 27
                if self.binn == 1:
                    indice_tab_t_corte = 28
            if self.sub_img == 256:
                if self.binn == 2:
                    indice_tab_t_corte = 29
                if self.binn == 1:
                    indice_tab_t_corte = 30 

        #Retorna os valores de readout da camera para todos os modos
        readout_times = self.read_tab_return_column(self.tab_valores_readout , 'Tempo critico')[1:31]
        #Seleciona um readout com base no modo de operacao
        self.t_corte = readout_times[indice_tab_t_corte]
        

    def calc_acquisition_rate(self):
        #Para t_exp < t_corte: interpola os dados da planilha
        #Para t_exp > t_corte: calcula 1/t_exp
        if self.t_exp < self.t_corte:
            self.calc_acquisition_rate_texp_lower_tcorte()
        if self.t_exp >= self.t_corte:
            self.calc_acquisition_rate_texp_greater_tcorte()


    def calc_texp_provided_acquisition_frequency(self, target_acquisition_frequency):
        acq_freq = target_acquisition_frequency 
        freq_corte = 1/self.t_corte        
        if acq_freq <= freq_corte:
            self.max_t_exp = 1/acq_freq
        if acq_freq > freq_corte:
            #nome da planilha com a curva de acq_rate x t_exp
            tab_name = self.define_acq_rate_tab_name()
            #retorna a coluna com o tempo de exposicao
            t_exp_column = self.read_tab_return_column(tab_name, 'TEXP (s)')
            t_exp_column = self.filter_list(t_exp_column)
            #retorna a coluna com a frequencia de aquisicao
            acq_rate_column = self.read_tab_return_column(tab_name, 'FREQ (fps)')
            acq_rate_column = self.filter_list(acq_rate_column)
            #print(t_exp_column,acq_rate_column) 
            #calcula o t_exp em função da frequência de aquisição fornecida            
            f = interp1d(acq_rate_column, t_exp_column)        
            self.max_t_exp = float(f(acq_freq))
            #print(self.max_t_exp)
        return self.max_t_exp


##ARC = AcquisitionRateCalc()
##ARC.write_operation_mode(1, 30, 1, 1024,  0.00001)
##ARC.seleciona_t_corte()
##ARC.calc_acquisition_rate()
##print('\nAcquisition Rate = ',ARC.acquisition_rate, 'Hz')
