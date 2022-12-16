# Odisseia
Investigação metodológica para a análise de dados de um dlis.

O objetivo deste repositório é explorar o conteúdo de um arquivo DLIS associado à um poço específico. Note que o objetivo é "casar" os dados do DLIS com o conteúdo da tabela de dados geoquímicos `exemplo Tabela poço 7-PIR-184D-AL.xlsx`.<br>

Como referência, utilize o documento em https://towardsdatascience.com/loading-well-log-data-from-dlis-using-python-9d48df9a23e2

e o manual de referência https://dlisio.readthedocs.io/en/latest/

## Dados de poços do CPRM:
Neste site encomtram-se apenas as bacias terrestres: https://reate.cprm.gov.br/

### TODO semana de 21-26 de novembro de 2022:

* [ @Layra ] ficar de stand by caso algum bug apareça por estarmos aplicando o programa em bacias com operadores diferentes. 
* [ @Felipe Dovales ] As propriedades de interesse que você deverá procurar, na variável channels, são: resistividade, condutividade, sônico (ou tempo de trânsito), raio gama, densidade, efeito fotoelétrico (NPHI - porosidade neutrônica), caliper. Uma vez que você as identificou, no channels, você deverá colocar o nome tal está escrito, na variável propriedades. Este procedimento criará uma lista contendo as variáveis de interesse. Compilar o programa até o final e salvar o arquivo de excel contendo as variáveis de interesse para o poço dlis da bacia de trabalho. 
* [ @Felipe Dovales ] Baixar para a sua máquina local os arquivos dlis das seguintes bacias: Para-Maranhão, Espírito Santo, Ceará, Sergipe-Alagoas. 
OBS: não esqueça de fazer as devidas mudanças relativas ao path e ao arquivo de saída para não sobrescrevê-los
* [ @Victor Carreira ] Aplicar a mesma metodologia para as Bacias Santos, Pelotas, Campos, Foz do Amazonas. 
