#!/usr/bin/env python
# coding: utf-8

# # CONVERTENDO AS CURVAS (CANAIS) DOS ARQUIVOS DLIS EM DATAFRAMES

# ### IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS

# In[42]:


import glob
from dlisio import dlis
import pandas as pd
from pandas import DataFrame, read_csv
import re
from collections.abc import Iterable
import numpy as np
import matplotlib.pyplot as plt
# modulos internos
import sys
sys.path.insert(0,'../modules')
from imod import Debug as db
from graficador import plotagem as plm2

# In[2]:


pd.set_option('display.max_rows', 7000)


# ### MAIS A SOBRE DLISIO: BIBLIOTECA PARA LEITURA E ANÁLISE DE DADOS DOS ARQUIVOS .DLIS:
# 
# https://dlisio.readthedocs.io/en/latest/

# ### FUNÇÕES UTILIZADAS

# #### FUNÇÃO PARA REMOVER VALORES REPETIDOS DE UMA LISTA

# In[2]:


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


# #### FUNÇÃO PARA DESENCADEAR LISTAS

# In[3]:


def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item


# #### FUNÇÃO QUE CRIA UM DATAFRAME CONTENDO PARÂMETROS DOS DLIS

# In[4]:


def summary_dataframe(object, **kwargs):
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


# #### FUNÇÃO PARA FILTRAR A PALAVRA ESCOLHIDA (PARÂMETRO FÍSICO) E RETORNAR UMA LISTA COM O NOME DOS CANAIS DO RESPECTIVO PARÂMETRO

# In[6]:


def filtro(dataframe, nome_canal):
    df_novo = dataframe[dataframe['Long Name'].str.contains(nome_canal)]
    lista = df_novo['Name'].to_list()
    return lista


# ### VARIÁVEIS ENCONTRADAS NO NOTEBOOK

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
# 

# ### LENDO OS ARQUIVOS DLIS

# In[7]:


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


# In[9]:


dicio_dlis


# In[10]:


#lendo os arquivos dlis com a biblioteca dlisio
lista_logicos1 = []
for i, v in dicio_dlis.items():
    f, *tail = dlis.load(dicio_dlis[i])
    tail.append(f)
    #colocando todos os arquivos lógicos na lista: lista_logicos1 
    lista_logicos1.append(tail)


# In[11]:


lista_logicos1


# In[12]:


#utilizando a função para desencadear a lista
lista_logicos2 = list(flatten(lista_logicos1))


# ### EXIBINDO O CABEÇALHO DOS 4 PRIMEIROS ARQUIVOS LÓGICOS DA LISTA_LÓGICOS2

# In[54]:


origin, *origin_tail = lista_logicos2[0].origins
#ver de qual dlis são esses logicos


# In[55]:


origin.describe()


# In[56]:


origin2, *origin_tail2 = lista_logicos2[1].origins
origin2.describe()


# In[57]:


origin3, *origin_tail3 = lista_logicos2[1].origins
origin3.describe()


# In[58]:


#A partir dessa quarto lógico, o cabeçalho é o mesmo.
origin4, *origin_tail4 = lista_logicos2[2].origins
origin4.describe()


# ### EXTRAINDO OS FRAMES DOS ARQUIVOS LÓGICOS

# In[13]:


lista_frames = []
for i in lista_logicos2:
    for fr in i.frames:
        lista_frames.append(fr)


# In[14]:


#manipulação para remover os frames duplicados sem alterar o type
df_frames = pd.DataFrame(lista_frames, index = lista_frames)
df_frames.index = df_frames.index.astype('string')
df_frames = df_frames[~df_frames.index.duplicated(keep = 'first')]


# In[15]:


lista_frames2 = df_frames[0].to_list()


# In[16]:


lista_frames2


# ### FILTRANDO OS CANAIS NECESSÁRIOS 

# Como a quantidade de curvas dentro dos arquivos dlis é muito grande, para diminuir a demanda computacional, é necessário filtrar as curvas que realmente serão utilizadas no projeto.

# #### APLICANDO A FUNÇÃO SUMMARY_DATAFRAME E CRIANDO UM DATAFRAME COM OS PARÂMETROS DOS CANAIS: LONG NAME, DIMENSION, UNITS, FRAME.

# A partir do parâmetro "Long Name", poderemos filtrar os nomes dos canais pelo parâmetro físico que ele representa.

# In[17]:


#aplicando a função summary dataframe
lista_sumario = []
for i in lista_logicos2:
    lista_sumario.append(summary_dataframe(i.channels, name='Name', long_name='Long Name', dimension='Dimension', units='Units', frame='Frame'))
    


# In[18]:


#concatenando todos os dataframes em somente um
channels = pd.concat(lista_sumario)


# In[19]:


#print(channels)
channels.to_excel(saida + bacia + poco + '/channels.xlsx',index=False)
channels.to_csv(saida + bacia + poco + '/channels.csv', header=False, index=False, sep='\t')



print('**********************************************')
print('Verificar o arquivo channels na pasta do poço!')
print('**********************************************')
db.pause()


# #### FILTRANDO OS CANAIS.

# Primeiramente, colocamos o nome da(s) propriedade(s) escolhida(s) na lista abaixo. Esse nome pode ser conferido no dataframe acima (Ctrl+f para verificar ortografia, letras maiúsculas e minúsculas, etc.)

# In[20]:

#lista que deve conter os nomes das propriedades físicas que o usuário deseja salvar
propriedades = input('Insira *Ipsis Litteris* os nomes das propriedades físicas de interesse separadas por espaço simples->').split()


#list(map(int, input('Insira *Ipsis Litteris* os nomes das propriedades físicas de interesse, entre aspas simples, na forma p1, p2, etc:').split()))

#[input('Insira *Ipsis Litteris* os nomes das propriedades físicas de interesse, entre aspas simples, na forma p1, p2, etc:').split('')]


print(propriedades)
#db.pause()
#db.stop()


# Após isso, utilizamos a função filtra_canais para filtrarmos os nomes dos canais que contém a propriedade escolhida e colocamos os resultados na lista_alvo.

# In[21]:


lista_alvo = []
for i in propriedades:
    #filra_canais(nome do dataframe com os parâmetros definida acima, i = cada propriedade da lista "propriedades")
    lista_alvo.append(filtro(channels, i))


# In[22]:


#utilizando a função para desencadear a lista
lista_alvo =  list(flatten(lista_alvo))


# In[23]:


lista_alvo


# In[24]:


#utilizando a função para remover os nomes repetidos
lista_alvo = remove_repetidos(sorted(lista_alvo))


# In[25]:


lista_alvo


# #### FILTRANDO A PROFUNDIDADE

# A variável profundidade pode vir com diversos nomes, como: TDEP, DEPTH, INDEX444, etc. Por isso, criamos uma lista que contém uma parte do Long Name (do mesmo modo que na filtragem de canais). Somente analisando o dataframe 'channels', conseguimos saber qual é a variável de profundidade.

# In[26]:


#no caso da Bacia do Amazonas, a string 'INDEX' aparece nos long names das profundidades.
profundidade = ['INDEX','TDEP','DEPT','DEPTH']


# In[29]:


lista_profundidade = []
for i in profundidade:
    #filra_canais(nome do dataframe com os parâmetros definida acima, i = cada propriedade da lista "propriedades")
    lista_profundidade.append(filtro(channels, i))


# In[30]:


#aplicando função para desencadear a lista
lista_profundidade = list(flatten(lista_profundidade))


# In[31]:


lista_profundidade


# In[32]:


#aplicando a função para remover os repetidos
lista_profundidade= remove_repetidos(sorted(lista_profundidade))


# In[34]:


lista_profundidade


# **OBS1.: CASO O DLIS CONTENHA O CANAL "TDEP", COLOQUE-O DIRETAMENTE NA LISTA_PROFUNDIDADE (NÃO HÁ PALAVRA CHAVE QUE FILTRE O TDEP)**
#     
# **DESSA FORMA:**
# 
# **lista_profundidade = ['TDEP']**

# **OBS2.: QUANDO A PROFUNDIDADE FOR 'TDEP', ELA GERALMENTE VEM EM PÉS. A CONVERSÃO DE PÉS PARA METROS É MULTIPLICAR O VALOR POR 0.00254 . ESSA MULTIPLICAÇÃO DEVERÁ SER COLOCADA NO CÓDIGO DE TRANFORMAR CURVAS EM DATAFRAMES ABAIXO (ESTÁ SINALIZADO NA CÉLULA).**

# ### CÓDIGO QUE TRANSFORMA OS VALORES DOS CANAIS EM DATAFRAME DE ACORDO COM A PROFUNDIDADE.

# Para aplicarmos a função, utilizaremos 4 listas: lista_logicos2, lista_frames2, lista_alvo e lista_profundidade.

# In[53]:


lista_curvas = []

for i in lista_logicos2:
    
    for fr in lista_frames2:

        try:

            #pegando as curvas de todos os frames
            curves = fr.curves()
            #curves = frame.curves()

        except Exception as err: 

            print(f' *O {i}, {fr} possui o erro: {err}*')
            pass

        for v in lista_alvo:

            curve_name = str(v) + '_' + str(i) + '_' + str(fr) 

            for profundidade in lista_profundidade:    

                try:

                    curvas = (pd.DataFrame(curves[v], columns = [curve_name], index = curves[profundidade]))
                    
                    #CASO A PROFUNDIDADE ESTEJA EM PÉS, UTILIZE:
                    #curvas = (pd.DataFrame(curves[v], columns = [curva_name], index = curves[profundidade]*0.00254))
                    #comente o curvas acima
                    
                    #transformando o valor -999.25 em nulo
                    curvas[curve_name][curvas[curve_name] == -999.250000] = np.nan
                    
                    lista_curvas.append(curvas)
                    
                    #para alertar quais lógicos possuem as curvas
                    #print(f'** O {i}, {fr} possui a curva {v}')


                except Exception as e: 

                    #print(f' O {i}, {fr}, possui o erro: {e}')
                    pass


# In[54]:


#removendo os valores contantes (erro comum no dado)
lista_curvas2 = []
for i in lista_curvas:
    lista_curvas2.append(i.reset_index().drop_duplicates(subset='index', keep='last').set_index('index').sort_index())


# In[55]:


#lista contendo todos os dataframes (cada dataframe é uma curva)
lista_curvas2


# In[56]:


curvas_alvo = pd.concat(lista_curvas2, axis = 1)


# In[57]:


curvas_sem_index = curvas_alvo.reset_index()


# In[58]:


print('Dimensão do arquivo com as propriedades alvo->',np.shape(curvas_sem_index))


#Salva o Dataframe:

curvas_sem_index.to_excel(saida + bacia + poco + '/alvos.xlsx' ,index=False)
curvas_sem_index.to_csv(saida + bacia + poco + '/alvos.csv',index=True, header=True, sep='\t', mode='a')

print('*******************************')
print('Verifique os arquivos de saída!')
print('*******************************')
