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


# In[41]:


dicio_dlis


# In[5]:


lista_logicos1


# In[6]:


#função para transformar listas encadeadas em listas
from collections import Iterable
def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item


# In[7]:


lista_logicos2 = list(flatten(lista_logicos1))


# In[8]:


lista_logicos2


# ### VENDO O CABEÇALHO DOS 4 PRIMEIROS ARQUIVOS LÓGICOS DA LISTA

# In[9]:


origin, *origin_tail = lista_logicos2[0].origins
#ver de qual dlis são esses logicos


# In[10]:


origin.describe()


# In[11]:


origin2, *origin_tail2 = lista_logicos2[1].origins
origin2.describe()


# In[44]:


origin3, *origin_tail3 = lista_logicos2[1].origins
origin3.describe()


# In[13]:


#A partir dessa quarto lógico, o cabeçalho é o mesmo.
origin4, *origin_tail4 = lista_logicos2[2].origins
origin4.describe()


# ### EXTRAINDO OS FRAMES DOS ARQUIVOS LÓGICOS

# In[14]:


lista_frames = []
for i in lista_logicos2:
    for fr in i.frames:
        lista_frames.append(fr)


# In[15]:


lista_frames


# In[16]:


#manipulação para remover os frames duplicados
df_frames = pd.DataFrame(lista_frames, index = lista_frames)
df_frames.index = df_frames.index.astype('string')
df_frames = df_frames[~df_frames.index.duplicated(keep = 'first')]


# In[17]:


lista_frames2 = df_frames[0].to_list()


# In[18]:


lista_frames2


# In[19]:


#extraindo somente as strings que estão dentro dos parênteses
lista_frames3 = []
for frame in lista_frames2:
       lista_frames3.append(str(frame)[str(frame).find("(")+1:str(frame).find(")")])


# In[20]:


lista_frames3


# ### EXTRAINDO OS CANAIS (CURVAS) DOS ARQUIVOS LÓGICOS 

# In[21]:


canais = []
for i in lista_logicos2:
    canais.append(i.channels)


# In[22]:


canais = list(flatten(canais))


# In[23]:


canais


# In[24]:


#extraindo somente as strings entre parênteses
canais2 = []
for ch in canais:
       canais2.append(str(ch)[str(ch).find("(")+1:str(ch).find(")")])


# In[25]:


canais2


# In[30]:


#revomendo os canais duplicados e colocando em ordem alfabetica
canais3 = list(sorted(set(canais2)))


# In[31]:


canais3


# ## EXTRAINDO AS CURVAS E TRANSFORMANDO EM DATAFRAMES

# In[51]:


canais_alvo = ['GR', 'EHGR']


# In[53]:


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
         
        for v in canais_alvo:
                
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


# In[54]:


#removendo as linhas com indices duplicados (são valores constantes realmente removidos das análises)
lista_curvas2 = []
for i in lista_curvas:
    lista_curvas2.append(i.reset_index().drop_duplicates(subset='index', keep='last').set_index('index').sort_index())


# In[50]:


lista_curvas2[899]


# In[36]:


len(lista_curvas2)


# In[37]:


#pegando alguns dataframes para teste
lis = [lista_curvas2[0], lista_curvas2[1000], lista_curvas2[3000]]


# In[55]:


#concatenando a lista de teste
curvas = pd.concat(lista_curvas2, axis = 1)


# In[56]:


curvas


# ### CRIANDO UM DATAFRAME COM TODOS OS CANAIS E SEUS RESPECTIVOS "LONG NAMES"

# In[59]:


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


# In[60]:


channels = summary_dataframe(f.channels, name='Name', long_name='Long Name',
                             dimension='Dimension', units='Units', frame='Frame')
channels


# ### FUNÇÃO PARA FILTRAR A PALAVRA ESCOLHIDA (PARÂMETRO FÍSICO) E RETORNAR UMA LISTA COM O NOME DOS CANAIS DO RESPECTIVO PARÂMETRO

# In[122]:


def lista_canais(dataframe, nome_canal):
    df_novo = dataframe[dataframe['Long Name'].str.contains(nome_canal)]
    lista = df_novo['Name'].to_list()
    return lista


# In[123]:


lista_gamma = lista_canais(df, 'Gamma')


# In[124]:


lista_gamma


# In[118]:


#FUNÇÃO PARA REMOVER VALORES REPETIDOS
def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


# In[125]:


lista_gamma = remove_repetidos(lista_gamma)


# In[126]:


lista_gamma


# ### APLICANDO O CÓDIGO NA NOVA LISTA

# In[127]:


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
         
        for v in lista_gamma: ###AQUI QUE APLICA A NOVA LISTA <-----------------------------
                
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


# In[131]:


lista_curvas2 = []
for i in lista_curvas:
    lista_curvas2.append(i.reset_index().drop_duplicates(subset='index', keep='last').set_index('index').sort_index())


# In[132]:


curvas_gamma = pd.concat(lista_curvas2, axis = 1)


# In[134]:


curvas_gamma

