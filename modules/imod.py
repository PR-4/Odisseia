#-*- coding: utf-8 -*-

# Oração segunda de S. Tomás de Aquino para o estudo:

#Criador Inefável,
#Vós que sois a fonte verdadeira da luz e da ciência,
#derramai sobre as trevas da minha inteligência um raio da vossa claridade.

#Dai-me inteligência para compreender,
#memória para reter,
#facilidade para aprender,
#sutileza para interpretar
#e graça abundante para falar.

#Meu Deus, semeai em mim a semente da vossa bondade.

#Fazei-me pobre sem ser miserável,
#humilde sem fingimento,
#alegre sem superficialidade,
#sincero sem hipocrisia;
#que faça o bem sem presunção,
#que corrija o próximo sem arrogância,
#que admita a sua correção sem soberba;
#que a minha palavra e a minha vida sejam coerentes.

#Concedei-me, Verdade das verdades,
#inteligência para conhecer-Vos,
#diligência para Vos procurar,
#sabedoria para Vos encontrar,
#uma boa conduta para Vos agradar,
#confiança para esperar em Vós,
#constância para fazer a Vossa vontade.

#Orientai, meu Deus, a minha vida;
#concedei-me saber o que me pedis
#e ajudai-me a realizá-lo
#para o meu próprio bem
#e de todos os meus irmãos.

#Amém.

#-------------------------------------------#
#  Organiza as minhas subrotinas dispersas. #
# Carreira,V.R.(2020)                       #
#-------------------------------------------#


#########PACOTES############
import os
import sys
import numpy as np
import pandas as pd
############################



class Debug:
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



class Preprocessing:
    pass

    def Winput():
        '''
        Generical method to read well log *.txt, *.las and *.csv data into a correct pandas Data Frame. 
        Input:
              - File name
              - Number of header lines (optional: use 0 instead)
              - Number of footer lines (optional: use 0 instead)
        Output:
              - df, Well Data into a Pandas Data Frame
              - Data Frame information
        '''
        
        file=str(input("File name="))
        sr=int(input("Header's line numbers="))
        sp=int(input("Footer's line numbers="))
        
        df = pd.read_csv(file , sep='\s+', skiprows=sr ,skipfooter=sp, index_col=0)
        
        #Inverte as linhas do dataframe e reseta os índices:
        df=df[::-1].reset_index()

        return df, print(df.info())
#-----------------------------------------
    def channels(df):# Verificar!!!
        '''
        Return the names of the log drilling channels inside data.
        Input: 
             -  df, Pandas Data Frame
        Output:
             - columns names
        '''

        for col_name in df.columns: 
            print(col_name)
        return df
#------------------------------------------
    def lcounter(channel):
        '''
        Count the number of samples in a rock class:
        Inputs:
           - channel, Pandas Data Frame of codes;
        Outputs:
           - k, counter
           - code, rock class 
        '''
        k=0
        code=int(input('Input code =' ))
        drill=np.asarray(channel)
        for i in range(len(drill)):
            if drill[i] == code:
                k=k+1
        return print('There is',k,'numbers of rock with code',code)
    
#-------------------------------------------
    def noncollapsed(dim,delta,cali,df):
        '''
        Search and filter noncollapsed well parts based on caliper analysis.
        Inputs:
               - dim, well's diameter
               - delta, acceptable well's diameter variation
               - cali, pd.DataFrame that contains caliper channel info
               - df, total dataframe info
        Outputs:
               - filtered data
        OBS: consider to use pd.read_csv method for input channels. 
        '''
        ls = dim + delta
        li = dim - delta
        df=df[( cali >= li) & ( cali <= ls)]

        return df

#--------------------------------------------
    def spurious(df,channel,a,b):
        '''
        Search and filter tool errors. Fixed inspired real experience.
        Inputs:
              - df, Pandas Data Frame
              - channel, channel to be filtered
              - a, could be a real or a dummy value
              - b, coudl be a real or a dummy value
        Output:
              - df, filtered data frame
        OBS: tools errors should be the same and constant values.      
        '''
        a = input('a =')
        b = input('b =')
        
        df=df[(channel != -a) &  (channel != -b)]

        return df

#--------------------------------------------
    def pd2np(channel):
        '''
        Transforms a pd.DataFrame channel into an array. Type variable transformator. 
        Input:
             - df, DataFrame channel type
        Output:
             - x, array type
        '''
        x = np.array(channel)

        return x

#------------------------------------------


def descompac(depht,channel,top=None,bottom=None):
    ''' Subroutine that corrects overburden stress.
        Inputs:
        -depht, depht information must be an array
        -channel, must be an array containing the physical property information
        -top, real top value (optional)
        -bottom, real bottom value (optional)
        Output:
        -descompac, channel corrected
    '''
    prof = []
    perf = []
    kk = []# vetor de índices
    
    if (top != None and bottom != None):
        k=0
        for i in range(len(depht)):
            if (depht[i] >= top and depht[i] <= bottom):
                kk.append(i)
                prof.append(depht[i])
                perf.append(channel[i])
                k+=1
                
                    
        ones=np.ones_like(np.array(prof))# cria um vetor de uns
        print(np.size(np.array(prof)))
        G=np.column_stack((np.array(prof),ones))#melhor método para juntar arrays 1D
        m = np.linalg.solve(np.dot(G.T,G),np.dot(G.T,np.array(perf)))
        # Cálculo de S (polinomial de grau 1 que calcula um novo conjunto de dados de perfilagem)
        S = m[0]*np.array(prof) + m[1]
        # Resíduo:
        PHI = (np.array(perf)-S) + np.mean(S) 
        for j in range(k):# substituindo o trecho corrigido no perfil original 
            channel[kk[j]] = PHI[j]
        
       
    
    
    else:
         # Estrutura o vetor de uns e a matriz sensibilidade
        ones=np.ones_like(depht)# cria um vetor de uns
        G=np.column_stack((depht,ones))#melhor método para juntar arrays 1D
        m = np.linalg.solve(np.dot(G.T,G),np.dot(G.T,channel))
       #Cálculo de S (polinomial de grau 1 que calcula um novo conjunto de dados de perfilagem)
        S = m[0]*prof + m[1]
        # Resíduo:
        PHI = (channel-S) + np.mean(S) 
       
    
    
    plt.figure(figsize=(25,5))
    plt.plot(prof,perf,color='red', marker='o', markersize=3, label='Perfil')
    plt.plot(prof,S,color='blue', marker='*', markersize=3,label='S')
    plt.plot(prof,PHI,color='green', marker='+', linestyle='dashed', linewidth=1, markersize=3,label='phi')
    plt.ylabel('Ajuste')
    plt.xlabel('Profundidade (m)')
    plt.gca().invert_yaxis()   
    plt.legend()
    plt.plot()

    
    return channel


#--------------------------------------------------

def overburden(depht,channel):
    ''' Subroutine that corrects overburden stress.
        Inputs:
        -depht, depht information must be an array
        -channel, must be an array containing the physical propertie information
        -top, real top value
        -bottom, real bottom value
        Output:
        -descompac, channel corrected
    '''
        
    # Estrutura o vetor de uns e a matriz sensibilidade
    ones=np.ones_like(depht)# cria um vetor de uns
    G=np.column_stack((depht,ones))#melhor método para juntar arrays 1D
    m = np.linalg.solve(np.dot(G.T,G),np.dot(G.T,channel))
    #Cálculo de S (polinomial de grau 1 que calcula um novo conjunto de dados de perfilagem)
    S = m[0]*prof + m[1]
    # Resíduo:
    PHI = (channel-S) + np.mean(S) 
    

    plt.figure(figsize=(25,5))
    plt.plot(depht,channel,color='red', marker='o', markersize=3, label='Perfil')
    plt.plot(depht,S,color='blue', marker='*', markersize=3,label='S')
    plt.plot(depht,PHI,color='green', marker='+', linestyle='dashed', linewidth=1, markersize=3,label='phi')
    plt.ylabel('Ajuste')
    plt.xlabel('Profundidade (m)')
    plt.gca().invert_yaxis()   
    plt.legend()
    
    
    return PHI


#--------------------------------------------------------------------------------

class Postprocessing:
    pass

    def error_counter (true,calculated):
        '''
         Error counter between true lithology and calculated lithology.
            Inputs:
              - true, array that contain true rock codes
              - calculated, array that contains modeled rock codes
            Output:
              - error, total error counter by an integer
              - p, porcentage error
          '''
        err=0  
        for i in range(len(true)):
            if true[i] != calculated[i]:
                err = err +1
            elif true[i] == calculated[i]: 
                err = err   
                
        p= (100*err)/len(true)
        
        return err, p

    
#------------------------------------------
class Statistical:
    pass
def rms(vetor):
    '''Root Mean Square 
    Input: 
    vetor, dados de COT
    Output:
    raiz, rms '''
    n = len(vetor)
    soma = 0.0
    raiz = 0.0
    media = 0.0
    for i in range(0, n):
        soma += (vetor[i] ** 2) # variável recebe sempre o valor anterior, igual ao i=i+1
    media = (soma/ (float)(n))
    raiz = media**(1/2)
    return raiz
            
    
def Pdiff(dado,h):
    '''Esta subrotina visa calcular a primeira derivada discreta progressiva
    de um vetor de entrada a cuja a dimensão é a malha com np pontos. 
    Entrada:
    dado, vetor com os dados
    h, tamanho da malha ou taxa de amostragem
    Saída:
    dp, vetor de derivada progressiva'''
    #variáveis internas
    fim=len(dado) #dimensão do dado -1 pq o python inicia a contagem no 0
    dp = np.zeros(fim) #cria um vetor vazio do tamanho do dado
    dado = np.array(dado) # transforma um dataframe em um array
    for i in range(fim-1):
        if i < fim-1:
            dp[i] = (dado[i+1]-dado[i])/h
        elif i == fim:
            dp[i]=dp[i-1] #tratamento do efeito de borda
        
    return dp

def Rdiff(dado,h):
    '''Esta subrotina visa calcular a primeira derivada discreta regressiva
    de um vetor de entrada a cuja a dimensão é a malha com np pontos. 
    Entrada:
    dado, vetor com os dados
    h, tamanho da malha ou taxa de amostragem
    Saída:
    dp, vetor de derivada regressiva'''
    #variáveis internas
    fim=len(dado) #dimensão do dado -1 pq o python inicia a contagem no 0
    dp = np.zeros(fim) #cria um vetor vazio do tamanho do dado
    dado = np.array(dado) # transforma um dataframe em um array
    for i in range(fim-1):
        if i < fim:
            dp[i] = (dado[i]-dado[i-1])/h
        elif i == fim:
            dp[i]=dp[i-1] #tratamento do efeito de borda
        
    return dp

def Cdiff(dado,h):
    '''Esta subrotina visa calcular a primeira derivada discreta central
    de um vetor de entrada a cuja a dimensão é a malha com np pontos. 
    Entrada:
    dado, vetor com os dados
    h, tamanho da malha ou taxa de amostragem
    Saída:
    dp, vetor de derivada central'''
    #variáveis internas
    fim=len(dado) #dimensão do dado -1 pq o python inicia a contagem no 0
    dp = np.zeros(fim) #cria um vetor vazio do tamanho do dado
    dado = np.array(dado) # transforma um dataframe em um array
    for i in range(fim-1):
        if i < fim:
            dp[i] = (dado[i+1]-dado[i-1])/2*h
        elif i == fim:
            dp[i]=dp[i-1] #tratamento do efeito de borda
        
    return dp

#----------------------------------------------------------
class COT:
    pass
def dlogr(res,x,m):
    '''Função que determina o Delta log R dos pares ordenados de propriedades
    Resistividade e Sônico ou Resistividade ou Densidade. 
    Entradas:
    res, dados de resistividade
    x, canal de densidade ou sônico
    m, coeficiente de cimentação
    Saída:
    DlogR, Delta Log R'''
    
    import math
    dado  = len(res)
    DlogR = np.zeros(dado)
    res   = np.array(res)
    x     = np.array(x)
    resb  = np.min(res)
    xb    = np.median(x)
    
    #Recurso computacional para eliminar os zeros:
    dummy = 1e-100000
    
    for i in range(dado):
        DlogR[i]=math.log10(res[i]/(resb+dummy))+((1/np.log(10))*(m/(x[i]-xb))*(x[i]-xb))
        if x[i]/xb < 0:
            print(x[i]-xb)
        if res[i]/resb < 0:
            print("Cuidado! Log negativo!",res[i]-resb)
     
        
    return DlogR


def dlogr90(res,resb,x,xb):
    
    
    if np.size(res) > 1:
        dado  = len(res)
        DlogR = np.zeros(dado)
        res   = np.array(res)
        x     = np.array(x)
        resb  = np.min(res)
        xb    = np.median(x)
        for i in range(dado):
            DlogR[i]=math.log10(res[i]/(resb))+(0.02*(x[i]-xb))
            if x[i]/xb < 0:
                print(x[i]-xb)
                if res[i]/resb < 0:
                    print("Cuidado! Log negativo!",res[i]-resb)
    else:
        res = float(res)
        resb = float(resb)
        x = float(x)
        xb = float(xb)
        DlogR=math.log10(res/(resb))+(0.02*(x-xb))
        
    return DlogR

def passey16(drlog,alfa,beta,delta,eta,Tmax,gr):
    '''Função que determina COT via delta log R
        Entradas:
    drlog,parâmetro calculado
    alfa, parâmetro estimado
    beta, parâmetro estimado
    delta, parâmetro estimado
    eta, parâmetro estimado
    Tmax, indicador de maturidade em oC
    gr, canal raio gama
    Saída:
    COT, Conteúdo orgânico total
    '''
    dado = len(gr)
    COT  = np.zeros(dado)
    gr   = np.array(gr)
    grb  = np.median(gr) 
    
    for i in range(dado):
        COT[i] = (alfa*drlog[i] + beta*(gr[i]-grb))*10**(delta-eta*Tmax)
        #print(COT[i],delta-eta*Tmax)
            
    return COT
    
    
#-------------------------------------------------------------------------
class achilles:
    pass
    
def igr(GR):
    GRmin=min(GR)
    GRmax=max(GR)
    IGR = np.zeros(np.size(GR))
    IGR = (GR-GRmin)/(GRmax-GRmin)
    return IGR

def clavier(IGR):
    VSH = np.zeros(np.size(IGR))
    VSH = 1.7 - np.sqrt(3.38-(IGR+0.7)**2.0)
    return VSH

def SandFraction(VSH):
    SF= (1-VSH) * 100
    return SF

def DensidadeAparenteSeca(RHOB,NPHI):
    NPHI= NPHI / 100 # Fator de conversão
    DAS=RHOB-NPHI
    return DAS 


