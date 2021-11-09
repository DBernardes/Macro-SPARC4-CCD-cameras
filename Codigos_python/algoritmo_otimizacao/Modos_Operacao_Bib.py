#!/usr/bin/env python
# coding: utf-8

# Classe ModosOperacao criada para armazenar os modos de operacao da camera permitidos.
# Estes modo sao obtidos atraves de uma operacao anterior e escritos dentro da classe.
# Esta classe possui como atributos o em_mode, em_gain, hss, binn, preamp, sub_img e t_exp.
# Esta classe permite escrita do modo de operacao e leitura tanto de valores individuais,
# como de todo o modo.

#24/10/2019. Denis Varise Bernardes.


class ModosOperacao:

    def __init__(self):
        self.em_mode = []
        self.em_gain = []
        self.hss = []
        self.preamp = []
        self.binn = []
        self.sub_img = []
        self.t_exp = []
        
        self.modos_operacao = []
        self.modo_atual = {}


    def write_mode(self, em_mode, em_gain, hss, preamp, binn, sub_img, max_t_exp, min_t_exp = 0.00001):        
        dic ={'em_mode':em_mode, 'em_gain':em_gain, 'hss':hss, 'preamp':preamp, 'binn':binn, 'sub_img':sub_img, 'max_t_exp':max_t_exp, 'min_t_exp':min_t_exp}
        self.modos_operacao.append(dic)

    def write_list_of_modes(self, lista):
        self.modos_operacao = lista

    def get_list_of_modes(self):
        return self.modos_operacao

    def clear_list_of_modes(self):
        self.modos_operacao = []

    
            
            
   



