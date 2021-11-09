#!/usr/bin/env python
# coding: utf-8

# Este código para a determinacao do
# modo de operacao de uma camera iXon Ultra 888 que otimize o ruido
# de leitura, a taxa de aquisicao, ou ambos.

#25/10/2019. Denis Varise Bernardes.

img_dir =r'C:\Users\observer\Desktop\Imagens_CCD'


from sys import exit
import Optimize_Operation_Mode as OOM
#Cria a classe que otimiza o modo de operação
OOM = OOM.Optimize_Operation_Mode(img_dir)
#verifica se os modos fornecidos de sub_img e binning estao corretos
OOM.verify_provides_modes()
#Esta opção serve para o cálculo do fluxo da estrela
OOM.calc_star_flux()
#Fixar(1-SNR, 2-Freq. Acq., 3-Ambos)
OOM.optimize(3)



