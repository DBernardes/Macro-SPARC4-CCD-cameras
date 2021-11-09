#!/usr/bin/env python
# coding: utf-8

# Esta biblioteca contem a classe que calcula a relacao sinal-ruido de uma das imagens do janderson,
# assim como o fluxo de fotons da estrela e do ceu.
#Denis Varise Bernardes.
#26/11/2019.

from math import exp, sqrt
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import numpy as np
from sys import exit
import Read_Noise_Calculation_Bib as RNC
import pandas as pd

class PhotonFluxCalc:

    def __init__(self, img_name, bias_name, xy_star, sky_radius, ccd_serial = 9916):        
        self.exp_time = 0
        self.n_pixels_object = 1
        self.sky_flux = 0
        self.dark_noise = 0
        self.read_noise = 0
        self.SNR = 0
        self.img_name = img_name
        self.x = xy_star[0]
        self.y = xy_star[1]
        self.sky_radius = sky_radius
        self.star_radius = 0
        self.img_data = 0
        self.sky_flux = 0
        self.sky_var = 0        
        self.ym, self.xm = [[]],[[]]
        self.star_flux = 0
        self.star_var = 0
        self.ganho = 0
        self.ccd_serial = ccd_serial
        self.bias_level = 0
        self.bias_name = bias_name


    def read_bias_img(self):
        bias_data = fits.getdata(self.bias_name)
        self.bias_level = np.median(bias_data)
        
    def read_img_get_info(self):
        #Esta funcao faz a leitura da imagem fornecida,
        # cria uma mascara com o tamanho da imagem
        # e dois arrays de indices com o tamanho da imagem
        # Tambem sao calculados os valores do ruido de RN e DC para o modo de operacao
        try:
            self.img_data = fits.getdata(self.img_name)[0]
            header = fits.getheader(self.img_name)
            img_shape = self.img_data.shape
            self.working_mask = np.ones(img_shape,bool)
            self.ym, self.xm = np.indices(img_shape, dtype='float32')
        except:
            self.img_data = fits.getdata(self.img_name)
            header = fits.getheader(self.img_name)
            img_shape = self.img_data.shape
            self.working_mask = np.ones(img_shape,bool)
            self.ym, self.xm = np.indices(img_shape, dtype='float32')

        #------------------------------------------------------------------------------
        try:
            string_ccd_temp = header['temp'].split(',')
            string_ccd_temp = string_ccd_temp[0] + '.' + string_ccd_temp[1]
            ccd_temp = float(string_ccd_temp)
        except:
            string_ccd_temp = header['temp']            
            ccd_temp = float(string_ccd_temp)
        
        
        #equacao tirada do artigo de caract. dos CCDs
        if self.ccd_serial == 9914:
            self.dark_noise = 24.66*exp(0.0015*ccd_temp**2+0.29*ccd_temp) 
        if self.ccd_serial == 9915:
            self.dark_noise = 35.26*exp(0.0019*ccd_temp**2+0.31*ccd_temp)
        if self.ccd_serial == 9916:
            self.dark_noise = 9.67*exp(0.0012*ccd_temp**2+0.25*ccd_temp)
        if self.ccd_serial == 9917:
            self.dark_noise = 5.92*exp(0.0005*ccd_temp**2+0.18*ccd_temp)

        #------------------------------------------------------------------------------
        try:
            string_texp = header['exposure'].split(',')
            string_texp = string_texp[0] + '.' + string_texp[1]        
            self.exp_time = float(string_texp)
        except:
            string_texp = header['exposure']                 
            self.exp_time = float(string_texp)
        #------------------------------------------------------------------------------
                
        hss = int(1/(float(header['readtime'])*1e6)) #em MHz
        
        try:preamp = int(header['preamp'].split('x')[0])
        except:preamp = int(header['preamp'])
        
        binn = int(header['hbin'])
        em_mode = header['outptamp']        
        if em_mode == 'Conventional':em_mode=0
        else:em_mode=1
        
        #em_mode = [em_mode, 2, hss, preamp, binn] # a variavel eh passada dessa forma por causa do funcionamento da hyperopt        
        RN = RNC.ReadNoiseCalc()
        #print(em_mode,hss,preamp,binn),exit()
        RN.write_operation_mode(em_mode, 2, hss, preamp, binn)        
        RN.calc_read_noise()
        #RN.get_operation_mode(),exit()
        self.read_noise = float(RN.noise)
        #print(self.read_noise),exit()

        #------------------------------------------------------------------------------
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
        
        

        

    def calc_star_sky_flux(self):
        # Esta funcao calcula o SNR ótimo
        self.read_img_get_info()
        max_snr = 0
        max_radius = 0
        max_flux = 0
        max_pixels = 0
        sky_flux = 0
        for star_radius in range(1, self.sky_radius):            
            self.calc_sky_flux(star_radius)
            self.calc_star_flux(star_radius)
            self.calc_SNR()
            #print(self.SNR, star_radius)
            if self.SNR > max_snr :
                max_snr = self.SNR
                max_radius = star_radius
                max_flux = self.star_flux
                max_pixels = self.n_pixels_object
                sky_flux = self.sky_flux
        self.star_radius = max_radius
        self.SNR = max_snr
        self.star_flux = max_flux       
        self.n_pixels_object = max_pixels
        self.sky_flux = sky_flux
        #print('\n', self.SNR, self.star_flux)

        
    def calc_sky_flux(self, start_radius):
        # Esta funcao calcula a quantidade de fluxo na regiao do ceu
        img = self.img_data        
        r = np.sqrt((self.xm - self.x)**2 + (self.ym - self.y)**2)
        sky_mask = (r > 2* self.sky_radius) * (r < 3 * self.sky_radius) * self.working_mask        
        self.sky_flux = np.median(img[np.where(sky_mask)])
        self.sky_var = np.median(np.abs(img[np.where(sky_mask)] - self.sky_flux)) / 0.674433
        #print(self.sky_flux)


    def calc_star_flux(self, start_radius) :
        # Esta funcao calcula a quantidade de flux da estrela
        img = self.img_data              
        r = np.sqrt((self.xm - self.x)**2 + (self.ym - self.y)**2)    
        star_mask = (r < start_radius) * self.working_mask        
        self.star_flux = (img[np.where(star_mask)] - self.sky_flux).sum()
        self.star_var = (img[np.where(star_mask)] + self.sky_var).sum()
        self.n_pixels_object = len(img[np.where(star_mask)])        
        
    def calc_SNR(self):
        #Esta funcao calcula o SNR da estrela
        gain = self.gain        
        self.sky_flux = self.sky_flux - self.bias_level
        #print(self.star_flux, gain, self.n_pixels_object, self.sky_flux,  self.read_noise),exit()
        
        em_gain = 1 #testes da SNR com o emgain
        
        self.star_flux*=em_gain
        self.sky_flux*=em_gain
        self.dark_noise*=em_gain
        
        aux = np.sqrt(self.star_flux*gain + self.n_pixels_object * (self.sky_flux*gain + self.dark_noise*self.exp_time + self.read_noise**2))
        self.SNR = self.star_flux*gain/aux        


    def get_results(self):
        n_pixels = self.n_pixels_object
        t_exp = self.exp_time
        dc = self.dark_noise*t_exp
        rn = self.read_noise
        snr = self.SNR        
        std_bias = 276.608517296231 #ADU        
        sky_flux = self.gain * (self.sky_flux) / t_exp - dc
        sky_var = self.gain * self.sky_var / t_exp        
        star_flux = self.gain * self.star_flux / t_exp
        star_var = self.gain * self.star_var / t_exp
        star_radius = self.star_radius
        return dc, rn, snr, sky_flux, sky_var, star_flux, star_var, n_pixels, star_radius
        

##PFC = PhotonFluxCalc(img_name = 'hats-24_I_transito_001.fits', bias_name = 'bias_final_002.fits', xy_star = (507,369), sky_radius=24, ccd_serial=9916)
##PFC.read_bias_img()
##PFC.calc_star_sky_flux()
##dc, rn, snr, sky_flux, sky_var, star_flux, star_var, n_pixels_star, star_radius = PFC.get_results()
###print(rn, snr, sky_flux, star_flux, n_pixels_star)
##print('\n')
##print('SNR:', snr)
##print('Sky Flux: ', sky_flux, 'photons/s')
##print('Star Flux:', star_flux, 'photons/s')
##print('Star Pixels:', n_pixels_star)
##print('Star Radius:', star_radius)
