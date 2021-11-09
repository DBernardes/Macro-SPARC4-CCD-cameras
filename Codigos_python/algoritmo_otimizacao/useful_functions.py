#!/usr/bin/env python
# coding: utf-8

# Este código reunie um conjunto de funções úteis na determinação
# do modo de operação ótimo dos CCDs.

#10/01/2020. Denis Varise Bernardes.

from sys import exit

def create_arq_obs_setup(img_dir):
    try:
        arq = open(img_dir + '\\' + 'observation_setup.txt', 'r')
    except:
        print('Preencha o arquivo contendo a configuração da observação.')        
        s ='''Arquivo contendo a configuracao da observacao a ser otimizada
-------------------------------------------------------------

Relacao sinal-ruido = 10
Taxa de aquisicao (Hz) = 1
Magnitude do objeto = 8 
Modos de sub-imagem = 1024,512,256
Binings dos pixieis = 1,2
Numero serial do CCD = 9917
Temperatura do CCD (oC) = -70 
Numero de iteracao do MOB = 100
Exportar configuracao para txt (s/n)? = s


Configuracoes da pre-imagem
----------------------------

Utilizar pre-imagem (s/n) = n 
Nome da imagem do objeto = 
Coordenadas do objeto (x,y) = 
Nome da imagem de bias = 
Raio maximo do ceu = 
        '''
        arq = open(img_dir + '\\' + 'observation_setup.txt', 'w')
        arq.write(s)
        arq.close()
        exit()
        
        
def get_obs_setup(img_dir):
    create_arq_obs_setup(img_dir)
    #Parâmetros da observação
    snr = 0
    acq_rate = 0
    obj_magnitude = 0
    sub_img_modes = 0
    binn_modes = 0    
    serial_number = 0
    ccd_temp= 0
    n_pix_star = 0    
    max_evals = 0
    fixar_param = 0
    export_arq = ''

    use_pre_img = ''
    pre_img_name = ''
    obj_coords = ()
    bias_img_name = ''
    sky_radius = 0
        
    arq = open(img_dir + '\\' + 'observation_setup.txt', 'r')
    lines = arq.read().splitlines()
    for line in lines:
        line = line.split('=')
        if 'Relacao sinal-ruido' in line[0]: snr = float(line[1])
        if 'Taxa de aquisicao' in line[0]: acq_rate = float(line[1])
        if 'Magnitude do objeto' in line[0]: obj_magnitude = float(line[1])
        if 'Modos de sub-imagem' in line[0]: sub_img_modes = [int(sub_img) for sub_img in line[1].split(',')]
        if 'Binings dos pixieis' in line[0]: binn_modes = [int(binn) for binn in line[1].split(',')]
        if 'Numero serial do CCD' in line[0]: serial_number = int(line[1])
        if 'Temperatura do CCD' in line[0]: ccd_temp = float(line[1])        
        if 'Numero de iteracao do MOB' in line[0]: max_evals = int(line[1])
        if 'Exportar configuracao para txt' in line[0]: export_arq = line[1]
        
        if 'Utilizar pre-imagem (s/n)' in line[0]: use_pre_img = line[1].strip()       
        if 'Nome da imagem do objeto' in line[0]:
            pre_img_name = line[1].strip()
            if '.fits' not in pre_img_name:pre_img_name+='.fits'        
        if 'Coordenadas do objeto' in line[0]: obj_coords = (int(line[1].split(',')[0]), int(line[1].split(',')[1]))
        if 'Nome da imagem de bias' in line[0]:
            bias_img_name = line[1].strip()
            if '.fits' not in bias_img_name:bias_img_name+='.fits'
        if 'Raio maximo do ceu' in line[0]: sky_radius = int(line[1])
        
        
    return  snr, acq_rate, obj_magnitude, sub_img_modes, binn_modes, serial_number, ccd_temp, max_evals, export_arq, use_pre_img, pre_img_name, obj_coords, bias_img_name, sky_radius
