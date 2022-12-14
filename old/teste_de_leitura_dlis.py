# -*- coding: utf-8 -*-
"""teste de leitura DLIS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PFdZh3suSRiDNaqiyQDTINinm7Du6K1d

O objetivo deste notebook é explorar o conteúdo de um arquivo DLIS associado à um poço específico. Note que o objetivo é "casar" os dados do DLIS com o conteúdo da tabela de dados geoquímicos `exemplo Tabela poço 7-PIR-184D-AL.xlsx`.<br>

Como referência, utilize o documento em https://towardsdatascience.com/loading-well-log-data-from-dlis-using-python-9d48df9a23e2

e o manual de referência https://dlisio.readthedocs.io/en/latest/

**É necessário montar o gdrive**
"""

# primeiro, é necessário instalar o dlisio
#!pip install dlisio

from dlisio import dlis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
f, *tail = dlis.load('Perfis_digitais/7-pir-184d-al_brsa_raw1.dlis')
print(f.describe())


for frame in f.frames:
    
    # Search through the channels for the index and obtain the units
    for channel in frame.channels:
        if channel.name == frame.index:
            depth_units = channel.units
    
    print(f'Frame Name: \t\t {frame.name}')
    print(f'Index Type: \t\t {frame.index_type}')
    print(f'Depth Interval: \t {frame.index_min} - {frame.index_max} {depth_units}')
    print(f'Depth Spacing: \t\t {frame.spacing} {depth_units}')
    print(f'Direction: \t\t {frame.direction}')
    print(f'Num of Channels: \t {len(frame.channels)}')
    print(f'Channel Names: \t\t {str(frame.channels)}')
    print('\n\n')

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

param_df = summary_dataframe(f.parameters, name='Name', long_name='Long Name', values='Value')

# Hiding people's names that may be in parameters.
# These two lines can be commented out to show them
mask = param_df['Name'].isin(['R8', 'RR1', 'WITN', 'ENGI'])
param_df = param_df[~mask]

print(param_df)

channels = summary_dataframe(f.channels, name='Name', long_name='Long Name',
                             dimension='Dimension', units='Units', frame='Frame')
print(channels)
