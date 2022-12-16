#-*- coding: utf-8 -*-

#--------------------------------------------#
# Módulo que contém as funções que investigam#
#os dados dlis e lis do programa odisseu e a #
#função acopladora.                          #
#--------------------------------------------#

####### PACOTES INTERNOS ###########
import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv
import re
import glob
from dlisio import dlis
from collections.abc import Iterable
import warnings
warnings.filterwarnings("ignore")
###################################

class debug:
    pass

def pause():
    '''
    FORTRANIC logical debugging. 
    Just for fortranic beings.
    '''
    programPause = input("Press the <ENTER> key to continue...")
    return

def stop():
    '''
    FORTRANIC logical debugging. 
    Just for fortranic beings.
    '''
    sys.exit('Stop here!')
    return


class odisseu:
    pass

def remove_repetidos(lista):
    '''
    FUNÇÃO PARA REMOVER VALORES REPETIDOS DE UMA LISTA
    INPUT: 
    - "lista": lista que contém elementos repetidos.

    OUTPUTs:
    - Lista sem elementos repetidos. 
    '''
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    
    return l

def flatten(lis):  
    '''
    FUNÇÃO PARA DESENCADEAR LISTAS
    INPUT: 
    - "lis": lista que é uma "lista de listas".
    OUTPUT:
    - Uma lista simples. 
    '''
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

def summary_dataframe(object, **kwargs):
    '''
    FUNÇÃO QUE CRIA UM DATAFRAME CONTENDO PARÂMETROS DOS DLIS
    INPUTS:  
    - "object": arquivo_lógico.object, onde object, no caso, será "Channel". 
    - "kwargs": atributos do objeto, escolhidos para compor o dataframe.

    OUTPUT:
    - Dataframe contendo os canais e seus atributos.

    Para saber mais sobre objetos e atributos da biblioteca Dlisio: https://dlisio.readthedocs.io/en/latest/dlis/api.html#basic-object 
    '''
    # Create an empty dataframe
    df = pd.DataFrame()

    # Iterate over each of the keyword arguments
    for i, (key, value) in enumerate(kwargs.items()):
        list_of_values = []
        # Iterate over each parameter and get the relevant key
        for item in object:
        # Account for any missing values.
            try:
                x = getattr(item, key)
                list_of_values.append(x)
            except:
                list_of_values.append('')
                continue
    
        # Add a new column to our data frame
        df[value]=list_of_values

        # Sort the dataframe by column 1 and return it
    return df.sort_values(df.columns[0])

def filtro(summary_df, nome_parametro):
    '''
    FUNÇÃO PARA FILTRAR A PALAVRA ESCOLHIDA (PARÂMETRO FÍSICO) E RETORNAR UMA LISTA COM O NOME DOS CANAIS DO RESPECTIVO PARÂMETRO
    INPUTS:
    - summary_df: dataframe gerado com a função summary_dataframe.
    - nome_parametro: nome ou parte do nome do parâmetro da curva. Ex.: "Gamma", "density". 
    
    OUTPUT:
    - Lista contendo o nome dos canais que contém o parâmetro físico escolhido. 
    '''

    df_novo = summary_df[summary_df['Long Name'].str.contains(nome_parametro)]
    lista = df_novo['Name'].to_list()
    return lista

def acoplador(dataframe_curvas, dataframe_litologias): 
    '''
    FUNÇÃO PARA ACOPLAR A LITOLOGIA NO DATAFRAME DE CURVAS
    INPUTS:
    - "dataframe_curvas": dataframe gerado com as curvas selecionadas.
    - "dataframe_litologias": dataframe gerado a partir do arquivo AGP.
    
    OUTPUT:
    - Dataframe das curvas com uma coluna contendo o nome da litologia e/ou uma coluna contendo o código da litologia
    de acordo com a profundidade. '''
    
    dataframe_litologias['Profundidade'] = dataframe_litologias['Profundidade'].astype(float)
    dataframe_curvas['lito'] = None
    dataframe_curvas['codigo_lito'] = np.nan
    curvas_min = dataframe_curvas[dataframe_curvas['index'] >= dataframe_litologias['Profundidade'].min()]
    
    if ('Code' in dataframe_litologias.columns) and ('Rock' in dataframe_litologias.columns):
        print('O DATAFRAME POSSUI AS COLUNAS CODE E ROCK')
        for i in dataframe_litologias.index:
            for j in dataframe_curvas['index']:
                try:
                    
                    if dataframe_litologias['Profundidade'][i] <= j < dataframe_litologias['Profundidade'][i+1]:
                        dataframe_curvas.loc[dataframe_curvas['index'] == j, 'lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Rock'].values[0]                   
                        dataframe_curvas.loc[dataframe_curvas['index'] == j, 'codigo_lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Code'].values[0]
                except Exception as e:
                    #print(f'erro do code e rock {e}')
                    pass
        
    elif ('Rock' in dataframe_litologias.columns) and ('Code' not in dataframe_litologias.columns):
        print('O DATAFRAME POSSUI SOMENTE A COLUNA ROCK')
        for i in dataframe_litologias.index:
            for j in dataframe_curvas['index']:
                try:
                    
                    if dataframe_litologias['Profundidade'][i] <= j < dataframe_litologias['Profundidade'][i+1]:
                        dataframe_curvas.loc[dataframe_curvas['index'] == j, 'lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Rock'].values[0]
                except Exception as e:
                    #print(f'erro do rock {e}')
                    pass
                
                
    elif ('Code' in dataframe_litologias.columns) and  ('Rock' not in dataframe_litologias.columns):
        print('O DATAFRAME POSSUI SOMENTE A COLUNA CODE')
        for i in dataframe_litologias.index:
            for j in dataframe_curvas['index']:
                try:
                    
                    if dataframe_litologias['Profundidade'][i] <= j < dataframe_litologias['Profundidade'][i+1]:
                        dataframe_curvas.loc[dataframe_curvas['index'] == j, 'codigo_lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Code'].values[0]
                except Exception as e:
                   # print(f'erro do code {e}')
                    pass
                
    return dataframe_curvas


