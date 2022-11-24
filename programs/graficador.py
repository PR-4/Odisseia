# -*- coding: utf-8 -*-
"""graficador.py
Autor(a): Victor
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1LqO4TBtrUc0rojI4taoPIhagejsk8hhC
"""
# PACOTES
import pandas as pd
import matplotlib.pyplot as plt




file = input('Digite o endereço e o nome do seu arquivo excel contendo os alvos:')
df = pd.read_excel(file)
print("Abra o arquivo excel com o nome alvos e copie e cole os nomes dos cabeçalhos que você quer graficar!!!")

plt.title("Gráfico verificador propriedade física X Profundidade")
plt.plot(df[input('Digite o nome do cabeçado do canal profundidade->')], df[input('Digite o nome do canal de interesse->')])
plt.show()