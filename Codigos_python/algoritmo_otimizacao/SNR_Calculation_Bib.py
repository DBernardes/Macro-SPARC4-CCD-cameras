#!/usr/bin/env python
# coding: utf-8

#Esta biblioteca determina os modos de operacao do CCD que atendem ao SNR fornecido
#Denis Varise Bernardes.
#26/11/2019.

from math import exp, sqrt
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np
from sys import exit
import Read_Noise_Calculation_Bib as RNC

class SignalToNoiseRatioCalc:

    def __init__(self, t_exp, em_mode, em_gain, hss, preamp, binn, ccd_temp, sky_flux, star_flux, n_pix_star, serial_number):       
        self.t_exp = t_exp
        self.em_mode = em_mode
        self.em_gain = em_gain
        self.hss = hss
        self.preamp = preamp
        self.binn = binn
        self.ccd_temp = ccd_temp
        self.sky_flux = sky_flux
        self.star_flux = star_flux
        self.n_pix_star = n_pix_star
        self.serial_number = serial_number
        
        self.dark_noise = 0
        self.SNR = 0
        self.gain = 0
        self.read_noise = 0        
        


    def calc_SNR(self):
        #Esta funcao calcula o SNR da estrela
        t_exp = self.t_exp
        em_gain = self.em_gain
        #Aplicação do ganho EM do CCD
        #Ganho EM = Ganho Real        
        if self.em_mode == 1:
            self.dark_noise *= em_gain
            self.star_flux *= em_gain
            self.sky_flux *= em_gain

        n_pix = self.n_pix_star
        dc = self.dark_noise
        rn = self.read_noise
        star = self.star_flux
        sky = self.sky_flux
        #print(star, t_exp, n_pix,rn,sky ,dc),exit()
        aux = np.sqrt(star*t_exp + n_pix * (rn**2 + (sky + dc)*t_exp ))        
        self.SNR = (star*t_exp) / aux


    #Esta função calcula o texp mínimo para uma dada SNR.
    #Na equação do SNR, isolei o texp, encontrando uma equação quadrática.
    #Calculo os termos a,b e c desta equação e, com isso, calculo suas raízes.
    #O texp será o valor mínimo não negativo encontrado.
    def calc_minimun_texp_provided_SNR(self, snr):               
        em_gain = self.em_gain
        #Aplicação do ganho EM do CCD
        #Ganho EM = Ganho Real        
        if self.em_mode == 1:
            self.dark_noise *= em_gain
            self.star_flux *= em_gain
            self.sky_flux *= em_gain

        n_pix = self.n_pix_star
        dc = self.dark_noise
        rn = self.read_noise        
        star = self.star_flux
        sky = self.sky_flux        
        a = star**2
        b = snr**2*(star+n_pix*(sky+dc))
        c = snr**2*n_pix*rn**2        
        minimun_t_exps = self.calc_quadratic_equation(a, -b, -c)       
        for t_exp in minimun_t_exps:
            if t_exp <= 0: minimun_t_exps.remove(t_exp)        
        return min(minimun_t_exps)

        

    def calc_quadratic_equation(self, a, b, c):
        delta = (b**2) - (4*a*c)
        x1 = (-b-sqrt(delta))/(2*a)
        x2 = (-b+sqrt(delta))/(2*a)
        return [x1,x2]
        


    def calc_DC(self):
        T = self.ccd_temp
        #equacao tirada do artigo de caract. dos CCDs
        # é calculado o dark noise direto da dark current obtida
        if self.serial_number == 9914:
            self.dark_noise = 24.66*exp(0.0015*T**2+0.29*T) 
        if self.serial_number == 9915:
            self.dark_noise = 35.26*exp(0.0019*T**2+0.31*T)
        if self.serial_number == 9916:
            self.dark_noise = 9.67*exp(0.0012*T**2+0.25*T)
        if self.serial_number == 9917:
            self.dark_noise = 5.92*exp(0.0005*T**2+0.18*T)        




    def calc_RN(self):
        #calcula o RN utilizando a biblioteca desenvolvida        
        RN = RNC.ReadNoiseCalc()    
        RN.write_operation_mode(self.em_mode, self.em_gain, self.hss, self.preamp, self.binn)
        RN.calc_read_noise()        
        self.read_noise =  float(RN.noise)




    def set_gain_value(self):
        #Configura o valor com ganho e-/ADU
        #do preamp com base no modo de operação
        em_mode = self.em_mode
        hss = self.hss
        preamp = self.preamp        
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



    def get_SNR(self):
        return self.SNR


    def print_noise_info(self):        
        print('\n------ Noise Info ------ ')
        print('Star Flux: ', self.star_flux, 'photons')
        print('Sky Flux: ', self.sky_flux, 'photons/pix')
        print('Read Noise: ', self.read_noise, 'e-/pix')
        print('Dark Noise: ', self.dark_noise, 'e-/pix')        


##SNRC = SignalToNoiseRatioCalc(t_exp = 0.00001,
##                              em_mode = 1,
##                              em_gain = 2,
##                              hss = 10,
##                              preamp = 1,
##                              binn = 1,
##                              ccd_temp = -70,
##                              sky_flux = 12.300419853836866, #e-/pix/s
##                              star_flux = 284.33043107743134, #1794.003737475248, #e-/pix/s
##                              n_pix_star = 305,
##                              serial_number = 9917)
##SNRC.set_gain_value()
##SNRC.calc_RN()
##SNRC.calc_DC()
##SNRC.calc_SNR()
##snr = SNRC.get_SNR()
##print('\nSNR = ', snr)
##SNRC.print_noise_info()
