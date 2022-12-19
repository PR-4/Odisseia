# Odisseia
Investigação metodológica para a análise de dados de um dlis.

O objetivo deste repositório é explorar o conteúdo de um arquivo DLIS associado à um poço específico. Note que o objetivo é "casar" os dados do DLIS com o conteúdo da tabela de dados geoquímicos `exemplo Tabela poço 7-PIR-184D-AL.xlsx`.<br>

Como referência, utilize o documento em https://towardsdatascience.com/loading-well-log-data-from-dlis-using-python-9d48df9a23e2

e o manual de referência https://dlisio.readthedocs.io/en/latest/

## Dados de poços do CPRM:
Neste site encomtram-se apenas as bacias terrestres: https://reate.cprm.gov.br/


## Metodologia

Para que o programa odsseu.py funcione de acordo como ele foi concebido é necessário seguir os passos da metodologia abaixo

```mermaid
flowchart TD

A(Baixar para sua máquina local os arquivos .dlis, .lis e agp.txt) -->|inputs| B(criar uma subpasta com o nome da bacia e outra com o nome do poço, dentro da pasta com o nome da bacia)
    B --> |outputs| C(repetir o processo acima para a pasta outputs)
    C --> |programs| D(executar no terminal o comando python odisseu.py)
    D --> E(inserir a localização dos arquivos conforme etapas A e B)
    E --> |outputs| F(verificar a profundidade no arquivo channels.xlsx ou channels.csv. )

               F{Requer análise do executor}
    F(comentar linha 271 e descomentar linha 274 para executar o fator de conversão) -->|Profundidade em pés| D(executar no terminal o comando python odisseu.py)
    F -->|Profundiade em metros| G[alimentar a lista propriedades com as propriedades alvo]

               G{Requer análise do executor}
   G --> |Havendo o arquivo agp| H[abrir o arquivo agp e inserir os índices das colunas e das linhas a serem excluídas no topo e na base do arquivo]   
   G --> |Não havendo o arquivo agp| I[digitar não no terminal e finalizar o processamento]


```
