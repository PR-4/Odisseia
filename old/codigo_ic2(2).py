#!/usr/bin/env python
# coding: utf-8

# # EXTRAINDO AS CURVAS DOS DLIS

# ### IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS

# In[1]:


import glob
from dlisio import dlis
import pandas as pd
import re


# ### LENDO OS ARQUIVOS DLIS

# In[2]:


path = 'dlis'


# In[3]:


lista_dlis = []
lista_read = []

#importando todos os arquivos dlis da pasta 'dlis'
for v, path_dlis in enumerate(glob.glob(f'{path}/*dlis')):
    lista_dlis.append(f'dlis_{v}')
    lista_read.append(path_dlis)

dicio_dlis = dict(zip(lista_dlis, lista_read))


# In[4]:


#lendo os arquivos dlis com a biblioteca dlisio
lista_logicos1 = []
for i, v in dicio_dlis.items():
    f, *tail = dlis.load(dicio_dlis[i])
    tail.append(f)
    #colocando todos os arquivos lógicos na lista_logicos1 
    lista_logicos1.append(tail)


# In[5]:


dicio_dlis


# In[6]:


lista_logicos1


# In[7]:


#função para transformar listas encadeadas em listas
from collections import Iterable
def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item


# In[8]:


lista_logicos2 = list(flatten(lista_logicos1))


# In[9]:


lista_logicos2


# ### VENDO O CABEÇALHO DOS 4 PRIMEIROS ARQUIVOS LÓGICOS DA LISTA

# In[10]:


origin, *origin_tail = lista_logicos2[0].origins
#ver de qual dlis são esses logicos


# In[11]:


origin.describe()


# In[12]:


origin2, *origin_tail2 = lista_logicos2[1].origins
origin2.describe()


# In[13]:


origin3, *origin_tail3 = lista_logicos2[1].origins
origin3.describe()


# In[14]:


#A partir dessa quarto lógico, o cabeçalho é o mesmo.
origin4, *origin_tail4 = lista_logicos2[2].origins
origin4.describe()


# ### EXTRAINDO OS FRAMES DOS ARQUIVOS LÓGICOS

# In[15]:


lista_frames = []
for i in lista_logicos2:
    for fr in i.frames:
        lista_frames.append(fr)


# In[16]:


lista_frames


# In[17]:


#manipulação para remover os frames duplicados
df_frames = pd.DataFrame(lista_frames, index = lista_frames)
df_frames.index = df_frames.index.astype('string')
df_frames = df_frames[~df_frames.index.duplicated(keep = 'first')]


# In[18]:


lista_frames2 = df_frames[0].to_list()


# In[19]:


lista_frames2


# In[20]:


#extraindo somente as strings que estão dentro dos parênteses
lista_frames3 = []
for frame in lista_frames2:
       lista_frames3.append(str(frame)[str(frame).find("(")+1:str(frame).find(")")])


# In[21]:


lista_frames3


# ### EXTRAINDO OS CANAIS (CURVAS) DOS ARQUIVOS LÓGICOS 

# In[22]:


canais = []
for i in lista_logicos2:
    canais.append(i.channels)


# In[23]:


canais = list(flatten(canais))


# In[24]:


canais


# In[25]:


#extraindo somente as strings entre parênteses
canais2 = []
for ch in canais:
       canais2.append(str(ch)[str(ch).find("(")+1:str(ch).find(")")])


# In[26]:


canais2


# In[27]:


#revomendo os canais duplicados e colocando em ordem alfabetica
canais3 = list(sorted(set(canais2)))


# In[28]:


canais3


# ### CRIANDO UM DATAFRAME COM TODOS OS CANAIS E SEUS RESPECTIVOS "LONG NAMES"

# In[31]:


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


# In[124]:


pd.set_option('display.max_rows', 7000)


# In[70]:


type(lista_logicos2[0])


# In[72]:


lista_sumario = []
for i in lista_logicos2:
    lista_sumario.append(summary_dataframe(i.channels, name='Name', long_name='Long Name', dimension='Dimension', units='Units', frame='Frame'))
    


# In[75]:


channels = pd.concat(lista_sumario)


# In[76]:


channels


# ### FUNÇÃO PARA FILTRAR A PALAVRA ESCOLHIDA (PARÂMETRO FÍSICO) E RETORNAR UMA LISTA COM O NOME DOS CANAIS DO RESPECTIVO PARÂMETRO

# In[33]:


def lista_canais(dataframe, nome_canal):
    df_novo = dataframe[dataframe['Long Name'].str.contains(nome_canal)]
    lista = df_novo['Name'].to_list()
    return lista


# In[114]:


#lista que deve conter os nomes das propriedades físicas que o usuário deseja salvar
propriedades = ['Resistivity', 'Sonic', 'Gamma']


# In[115]:


lista_alvo = []
for i in propriedades:
    lista_alvo.append(lista_canais(channels, i))


# In[116]:


lista_alvo =  list(flatten(lista_alvo))


# In[117]:


lista_alvo


# In[80]:


#FUNÇÃO PARA REMOVER VALORES REPETIDOS
def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


# In[118]:


lista_alvo = remove_repetidos(lista_alvo)


# In[105]:


lista_alvo


# ### APLICANDO O CÓDIGO NA NOVA LISTA

# In[119]:


lista_curvas = []

for i in lista_logicos2:
    
    for fr in lista_frames3:
        
        try:
            
            #pegando as curvas de todos os frames
            frame = i.object('FRAME', fr)
            curves = frame.curves()
        
        except Exception as err: 

            print(f' *O arquivo {i}, possui o erro: {err}*')
            pass
         
        for v in lista_alvo: ###AQUI QUE APLICA A NOVA LISTA <-----------------------------
                
            try:
                #colocando o nome da curva como o nome da curva + nome do logico  + nome do frame
                curva_name = v + '_' + str(i) + '_' + str(fr)
                #transformando as curvas em dataframes, onde o index é o TDEP convertido para metros
                curvas = pd.DataFrame(curves[v], columns = [curva_name], index = curves['TDEP']*0.00254)
                #colocando todos os dataframes em uma lista de dataframes
                lista_curvas.append(curvas)
                #para alertar quais lógicos possuem as curvas
                print(f'** O arquivo {i} possui a curva {v}')


            except Exception as e: 

                print(f' O arquivo {i}, possui o erro: {e}')
                pass


# In[120]:


lista_curvas2 = []
for i in lista_curvas:
    lista_curvas2.append(i.reset_index().drop_duplicates(subset='index', keep='last').set_index('index').sort_index())


# In[121]:


curvas_alvo = pd.concat(lista_curvas2, axis = 1)


# In[122]:


curvas_alvo = curvas_alvo.reset_index()


# In[123]:


curvas_alvo

