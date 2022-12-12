#!/usr/bin/env python
# coding: utf-8

# # CONVERTENDO AS CURVAS (CANAIS) DOS ARQUIVOS DLIS EM DATAFRAMES

# ### IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS



import glob
from dlisio import dlis
import pandas as pd
from pandas import DataFrame, read_csv
import re
from collections.abc import Iterable
import numpy as np
import time as t
import warnings
warnings.filterwarnings("ignore")
#modulos internos
import sys
sys.path.insert(0,'../modules')
from imod import Debug as db

# INÍCIO DO PROGRAMA

ini = t.time() # medindo o tempo de processamento

pd.set_option('display.max_rows',7000)


# ### MODULE:
# FUNÇÃO PARA REMOVER VALORES REPETIDOS DE UMA LISTA


def remove_repetidos(lista):
    
    '''INPUT: 
    - "lista": lista que contém elementos repetidos.
    
    OUTPUTs:
    - Lista sem elementos repetidos. '''
    
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


# FUNÇÃO PARA DESENCADEAR LISTAS

def flatten(lis):
    
    '''INPUT: 
    - "lis": lista que é uma "lista de listas".
    
    OUTPUT:
    - Uma lista simples. '''
    
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
            yield item


# FUNÇÃO QUE CRIA UM DATAFRAME CONTENDO PARÂMETROS DOS DLIS

def summary_dataframe(object, **kwargs):
    
    '''INPUTS:  
    - "object": arquivo_lógico.object, onde object, no caso, será "Channel". 
    - "kwargs": atributos do objeto, escolhidos para compor o dataframe.
    
    OUTPUT:
    - Dataframe contendo os canais e seus atributos.
    
    Para saber mais sobre objetos e atributos da biblioteca Dlisio: https://dlisio.readthedocs.io/en/latest/dlis/api.html#basic-object '''

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


# FUNÇÃO PARA FILTRAR A PALAVRA ESCOLHIDA (PARÂMETRO FÍSICO) E RETORNAR UMA LISTA COM O NOME DOS CANAIS DO RESPECTIVO PARÂMETRO

def filtro(summary_df, nome_parametro):
    
    '''INPUTS:
    - "summary_df": dataframe gerado com a função summary_dataframe.
    - "nome_parametro": nome ou parte do nome do parâmetro da curva. Ex.: "Gamma", "density". 
    
    OUTPUT:
    - Lista contendo o nome dos canais que contém o parâmetro físico escolhido. '''
    
    df_novo = summary_df[summary_df['Long Name'].str.contains(nome_parametro)]
    lista = df_novo['Name'].to_list()
    return lista


# FUNÇÃO PARA ACOPLAR A LITOLOGIA NO DATAFRAME DE CURVAS

def acoplador(dataframe_curvas, dataframe_litologias):
    
    '''INPUTS:
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
                    print(f'erro do code e rock {e}')
                    pass
        
    elif ('Rock' in dataframe_litologias.columns) and ('Code' not in dataframe_litologias.columns):
        print('O DATAFRAME POSSUI SOMENTE A COLUNA ROCK')
        for i in dataframe_litologias.index:
            for j in dataframe_curvas['index']:
                try:
                    
                    if dataframe_litologias['Profundidade'][i] <= j < dataframe_litologias['Profundidade'][i+1]:
                         dataframe_curvas.loc[dataframe_curvas['index'] == j, 'lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Rock'].values[0]
                   
                except Exception as e:
                    print(f'erro do rock {e}')
                    pass
                
                
    elif ('Code' in dataframe_litologias.columns) and  ('Rock' not in dataframe_litologias.columns):
        print('O DATAFRAME POSSUI SOMENTE A COLUNA CODE')
        for i in dataframe_litologias.index:
            for j in dataframe_curvas['index']:
                try:
                    
                    if dataframe_litologias['Profundidade'][i] <= j < dataframe_litologias['Profundidade'][i+1]:
                        dataframe_curvas.loc[dataframe_curvas['index'] == j, 'codigo_lito'] = dataframe_litologias.loc[dataframe_litologias.index == i, 'Code'].values[0]
           
                except Exception as e:
                    print(f'erro do code {e}')
                    pass
                
    return dataframe_curvas


#-------------------- ÍNDICE DE VARIÁVEIS ---------------------------------------#
#
# **dicio_dlis:** dicionário que contém todos os arquivos dlis da pasta selecionada
# 
# **lista_logicos1:** lista encadeada de todos os lógicos dos arquivos dlis
# 
# **lista_logicos2:** lista de todos os lógicos dos arquivos dlis
# 
# **lista_frames:** lista de todos os frames dos dlis
# 
# **lista_frames2:** lista sem nomes repetidos de todos os frames dos dlis
# 
# **lista_sumario:** lista contendo os dataframes com os parâmetros dos dlis
# 
# **channels:** dataframe com os parâmetros dos dlis
# 
# **propriedades:** lista onde o usuário coloca as propriedades físicas das curvas do filtro
# 
# **lista_alvo:** lista com o nome dos canais filtrados
# 
# **profundidade:** lista onde o usuário coloca uma string do Long Name da profundidade
# 
# **lista_profundidade:** lista com o nome dos canais de profundidade filtrados a partir da string anterior
# 
# **lista_curvas:** lista de dataframes, onde cada dataframe é uma curva (canal)
# 
# **lista_curvas2:** lista com os mesmos dataframes, mas sem os valores constantes
# 
# **curvas_alvo:** dataframe contendo todas as curvas com a profundidade indexada
# 
# **curvas_sem_indice:** dataframe contendo todas as curvas com a profundidade como coluna 
# --------------------------------------------------------------------------------

# LEITURA DOS ARQUIVOS DLIS

#colocar o nome da pasta, em formato de string, onde os arquivos dlis se encontram

entrada = '..'+'/'+'inputs'+'/'
saida = '..'+'/'+'outputs'+'/'
imagens = '..'+'/'+'images'+'/'
bacia = input('Entre com o nome da bacia sedimentar:') + '/'
poco = input('Entre com o nome do poço:') 

path = entrada + bacia + poco 


lista_dlis = []
lista_read = []

#importando todos os arquivos dlis da pasta '
for v, path_dlis in enumerate(glob.glob(f'{path}**/*dlis')):
    lista_dlis.append(f'dlis_{v}')
    lista_read.append(path_dlis)

#dicionário com todos os arquivos dlis que se encontram na pasta
dicio_dlis = dict(zip(lista_dlis, lista_read))


#lendo os arquivos dlis com a biblioteca dlisio
lista_logicos1 = []
for i, v in dicio_dlis.items():
    f, *tail = dlis.load(dicio_dlis[i])
    tail.append(f)
    #colocando todos os arquivos lógicos na lista: lista_logicos1 
    lista_logicos1.append(tail)



#utilizando a função para desencadear a lista
lista_logicos2 = list(flatten(lista_logicos1))




lista_logicos2


# ### EXIBINDO O CABEÇALHO DOS 4 PRIMEIROS ARQUIVOS LÓGICOS DA LISTA_LÓGICOS2


origin, *origin_tail = lista_logicos2[0].origins
#ver de qual dlis são esses logicos



origin.describe()



origin2, *origin_tail2 = lista_logicos2[1].origins
origin2.describe()



origin3, *origin_tail3 = lista_logicos2[1].origins
origin3.describe()



#A partir dessa quarto lógico, o cabeçalho é o mesmo.
origin4, *origin_tail4 = lista_logicos2[2].origins
origin4.describe()


# ### EXTRAINDO OS FRAMES DOS ARQUIVOS LÓGICOS


lista_frames = []
for i in lista_logicos2:
    for fr in i.frames:
        lista_frames.append(fr)



#manipulação para remover os frames duplicados sem alterar o type
df_frames = pd.DataFrame(lista_frames, index = lista_frames)
df_frames.index = df_frames.index.astype('string')
df_frames = df_frames[~df_frames.index.duplicated(keep = 'first')]



lista_frames2 = df_frames[0].to_list()



lista_frames2


# ### FILTRANDO OS CANAIS NECESSÁRIOS 

# Como a quantidade de curvas dentro dos arquivos dlis é muito grande, para diminuir a demanda computacional, é necessário filtrar as curvas que realmente serão utilizadas no projeto.

# #### APLICANDO A FUNÇÃO SUMMARY_DATAFRAME E CRIANDO UM DATAFRAME COM OS PARÂMETROS DOS CANAIS: LONG NAME, DIMENSION, UNITS, FRAME.

# A partir do parâmetro "Long Name", poderemos filtrar os nomes dos canais pelo parâmetro físico que ele representa.



#aplicando a função summary dataframe
lista_sumario = []
for i in lista_logicos2:
    lista_sumario.append(summary_dataframe(i.channels, name='Name', long_name='Long Name', dimension='Dimension', units='Units', frame='Frame'))
    



#concatenando todos os dataframes em somente um
channels = pd.concat(lista_sumario)


#print(channels)
channels.to_excel(saida + bacia + poco + '/channels.xlsx',index=False)
channels.to_csv(saida + bacia + poco + '/channels.csv', header=False, index=False, sep='\t')



print('**********************************************')
print('Verificar o arquivo channels na pasta do poço!')
print('**********************************************')
#db.pause()



# #### FILTRANDO OS CANAIS.

# Primeiramente, colocamos o nome da(s) propriedade(s) escolhida(s) na lista abaixo. Esse nome pode ser conferido no dataframe acima (Ctrl+f para verificar ortografia, letras maiúsculas e minúsculas, etc.)


#lista que deve conter os nomes das propriedades físicas que o usuário deseja salvar
propriedades = input('Insira *Ipsis Litteris* os nomes das propriedades físicas de interesse separadas por espaço simples->').split()


# Após isso, utilizamos a função filtra_canais para filtrarmos os nomes dos canais que contém a propriedade escolhida e colocamos os resultados na lista_alvo.

print(propriedades)
#db.pause()
#db.stop()


lista_alvo = []
for i in propriedades:
    #filra_canais(nome do dataframe com os parâmetros definida acima, i = cada propriedade da lista "propriedades")
    lista_alvo.append(filtro(channels, i))




#utilizando a função para desencadear a lista
lista_alvo =  list(flatten(lista_alvo))





#utilizando a função para remover os nomes repetidos
lista_alvo = remove_repetidos(sorted(lista_alvo))





lista_alvo


# #### FILTRANDO A PROFUNDIDADE

# A variável profundidade pode vir com diversos nomes, como: TDEP, DEPTH, INDEX444, etc. Por isso, criamos uma lista que contém uma parte do Long Name (do mesmo modo que na filtragem de canais). Somente analisando o dataframe 'channels', conseguimos saber qual é a variável de profundidade.




#no caso da Bacia do Amazonas, a string 'INDEX' aparece nos long names das profundidades.
profundidade = ['INDEX','TDEP','DEPT','DEPTH']





lista_profundidade = []
for i in profundidade:
    #filra_canais(nome do dataframe com os parâmetros definida acima, i = cada propriedade da lista "propriedades")
    lista_profundidade.append(filtro(channels, i))





#aplicando função para desencadear a lista
lista_profundidade = list(flatten(lista_profundidade))





#Caso haja o canal "TDEP", descomente o código abaixo e utilize-o para ser a lista_profundidade
#lista_profundidade = ['TDEP']





#aplicando a função para remover os repetidos
lista_profundidade= remove_repetidos(sorted(lista_profundidade))





lista_profundidade


# **OBS2.: QUANDO A PROFUNDIDADE FOR 'TDEP', ELA GERALMENTE VEM EM PÉS. A CONVERSÃO DE PÉS PARA METROS É MULTIPLICAR O VALOR POR 0.00254 . ESSA MULTIPLICAÇÃO DEVERÁ SER COLOCADA NO CÓDIGO DE TRANFORMAR CURVAS EM DATAFRAMES ABAIXO (ESTÁ SINALIZADO NA CÉLULA).**

# ### FUNÇÃO QUE TRANSFORMA OS VALORES DOS CANAIS EM DATAFRAME DE ACORDO COM A PROFUNDIDADE.

# Para aplicarmos a função, utilizaremos 4 listas: lista_logicos2, lista_frames2, lista_alvo e lista_profundidade.

# In[83]:


lista_curvas = []


for i in lista_logicos2:
    
    for fr in lista_frames2:
        
        try:

            #pegando as curvas de todos os frames
            curves = fr.curves()
            #curves = frame.curves()

        except Exception as err: 

            print(f' *O arquivo {i}, frame {fr} possui o erro: {err}*')
            pass

        for v in lista_alvo:

            curve_name = str(v) + '_' + str(i) + '_' + str(fr) 

            for profundidade in lista_profundidade:    

                try:

                    curvas = (pd.DataFrame(curves[v], columns = [curve_name], index = curves[profundidade]))
                    
                    #CASO A PROFUNDIDADE ESTEJA EM PÉS, UTILIZE:
                    #lista_curvas.append(pd.DataFrame(curves[v], columns = [curva_name], index = curves[profundidade]*0.00254))
                    
                    #transformando o valor -999.25 em nulo
                    curvas[curve_name][curvas[curve_name] == -999.250000] = np.nan
                    
                    lista_curvas.append(curvas)
                    
                    #para alertar quais lógicos possuem as curvas
                    #print(f'** O arquivo {i}, frame {fr}, possui a curva {v}')


                except Exception as e: 

                    #print(f' O arquivo {i}, frame {fr}, possui o erro: {e}')
                    pass



#removendo os valores constantes (erro comum no dado)
lista_curvas2 = []
for i in lista_curvas:
    lista_curvas2.append(i.reset_index().drop_duplicates(subset='index', keep='last').set_index('index'))





lista_curvas2





curvas_alvo = pd.concat(lista_curvas2, axis = 1)





#resetando o index e ordenando os valores em profundidade crescente 
curvas = curvas_alvo.reset_index().sort_values('index')



print('Dimensão do arquivo com as propriedades alvo->',np.shape(curvas))

#Salva o Dataframe:

curvas.to_excel(saida + bacia + poco + '/alvos.xlsx' ,index=False)
curvas.to_csv(saida + bacia + poco + '/alvos.csv',index=True, header=True, sep='\t', mode='a')



fim = t.time()
tempo = (fim-ini)/60
print("Tempo de processamento = ", tempo, "minutos")


print('*******************************')
print('Verifique os arquivos de saída!')
print('*******************************')





# ACOPLANDO A LITOLOGIA: EXPERIMENTAL!!!!!

acopla = input('Você deseja acoplar a litologia AGP?(sim ou não)->')
if acopla == 'sim':
    path = entrada + bacia + poco
    #path = 'agps'
    lista_agp = []
    #importando todos os arquivos dlis da pasta '
    for i in (glob.glob(f'{path}**/*txt')):
        lista_agp.append(i)

    print(lista_agp[0])
    
    # É IMPORTANTE QUE O NOME DAS COLUNAS SEJAM SEMPRE ('Profundidade', 'Code', 'Rock'), POIS A FUNÇÃO PARA  ACOPLAR POSSUI CONDICIONAIS QUE DEPENDEM DESSES NOMES
    db.pause()
    #lito = pd.read_csv(lista_agp[0], sep='\s+', usecols=(0,2,3), index_col=False, na_values= ' ', skiprows=1, names=('Profundidade', 'Code', 'Rock'))#, encoding = "UFT-8" ) 
    P = int(input('Insira o índice da coluna profundidade ->'))
    C = int(input('Insira o índice da coluna código ->'))
    R = int(input('Insira o índice da coluna rocha->')) 
    lito = pd.read_csv(lista_agp[0], sep='\s+', usecols=[P,C,R], index_col=False, na_values= ' ', skiprows=1, names=('Profundidade', 'Code', 'Rock'), encoding = "ISO-8859-1" )
    #print(lito) OK!!!!
    # FILTRANDO A PARTE DO DATAFRAME QUE CONTÉM AS INFORMAÇÕES NECESSÁRIAS: LITOLOGIA, CODE E ROCK
    init = int(input('Insira índice do topo da descrição do poço ->'))
    final = int(input('Insira índice da base da descrição do poço ->'))
    litologia = lito.loc[init:final] 
    print(litologia)
    db.stop()
    curvas_lito = acoplador(curvas, litologia) # função acopladora
    #Salva o Dataframe:
    curvas_lito.to_excel(saida + bacia + poco + '/alvosAGP.xlsx' ,index=False)
    curvas_lito.to_csv(saida + bacia + poco + '/alvosAGP.csv',index=True, header=True, sep='\t', mode='a')
    print('*******************************')
    print('--------Dados Acoplados!-------')
    print('*******************************')

else:
    print('*******************************')
    print('-------------FIM---------------')
    print('*******************************')
