# Odisseia
Criação de um banco de dados direcional.

O objetivo deste repositório é explorar o conteúdo de um arquivo DLIS associado à um poço específico. Note que o objetivo é "casar" os dados do DLIS com o conteúdo da tabela de dados geoquímicos `exemplo Tabela poço 7-PIR-184D-AL.xlsx`.<br>

Como referência, utilize o documento em https://towardsdatascience.com/loading-well-log-data-from-dlis-using-python-9d48df9a23e2

e o manual de referência https://dlisio.readthedocs.io/en/latest/

## Dados de poços do CPRM:
Neste site encomtram-se apenas as bacias terrestres: https://reate.cprm.gov.br/


## Metodologia

Para que o programa odisseu.py funcione de acordo como ele foi concebido é necessário seguir os passos da metodologia abaixo

```mermaid
flowchart TD

A(Baixar para sua máquina local os arquivos \n .dlis, .lis e agp.txt) --> B(Na pasta inputs, criar uma subpasta com o nome da bacia e \n uma subsub pasta com o nome do poço.)
    B --> C(Repetir o processo acima para na outputs)
    C --> D(Executar no terminal o comando python odisseu.py)
    D --> E(Verificar o arquivo channels.xlsx ou channels.csv. ) 
    E --> F(Checar a unidade da profundidade medida. Caso a profundiade esteja em pés, \n comente linha 271 e descomente linha 274 para executar o fator de conversão. \n Caso a profundidade esteja em metros siga com o processamento)
    F --> G(Alimente a lista de propriedades com as propriedades físicas alvo)
    G --> H{Acoplador}
    H --> |Havendo o arquivo agp| I(Abrir o arquivo agp e inserir os índices das colunas e das linhas \n a serem excluídas no topo e na base do arquivo)   
    H --> |Não havendo o arquivo agp| J(Digitar não, no terminal, e finalizar o processamento])


```
