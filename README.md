TCC - UM ESTUDO APLICADO A CARTEIRA DE INVESTIMENTOS EM FUNDOS IMOBILIÁRIOS

Trabalho feito por Victor Augusto de Souza Fonseca e Diego Patrick Fernandes Bastos

Sob Orientação de Prof. D. Sc. Sérgio Assunção Monteiro  

Passo a passo para instalação do codigo:

O codigo já está com o ambiente virtualizado do Python logo não é necessario se preocupar com as dependencias, unica coisa que é necessario é:

1 - Ter o python 3.6 ou maior instalado.

2 - Ter o MySQL 5.6 instalado

2.1 - Utilizamos o docker para usar o MySQL, porém se você tiver o banco na mesma versão instalado 
a usabilidade é o mesma só deve alterar a variavel "port" no arquivo "connectionDatabase.py"

2.2 - Caso queira utilizar o docker já temos um codigo, pronto para executar em sua maquina após ter instalado o docker:
docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

3 - A copia dos Databases utilizados foram exportados e se encontram no git.

Para utilizar o algoritmo as variaveis que precisam ser mudadas no arquivo "execute.py" de acordo com sua vontade são:

cod_fii = Ver os fundos disponiveis para sua analise.

valor_investido = O nome já autoexplicativo, é aqui onde você pode definir quanto dinheiro será investido em sua analise.

grafico = As opções são 1 e 2, 1 para o grafico de linhas e 2 para o grafico de pontos

data_inicio = Aqui é onde você definirá a data inicial de seu estudo com a data limite entre 2017-01-01 e 2021-09-06.

data_fim = Aqui é onde você definirá a data fim de seu estudo com a data limite entre 2017-01-01 e 2021-09-06.

Após isso só executar o script "execute.py" e você obterá suas analises.


-----------------------------------------------------------------------------------------------------------------------------------------------------------

                                                DISCLAIMER

Seguindo os principios do open scource este codigo pode ser modificado, reutilizado e aproveitado em diversos projetos sinta livre para utilizá-lo.

Obs: Nenhum dos ativos ou analises feitas ou citadas nesse trabalho são recomendações de compra ou venda, 
por favor estude e tome suas decisões quanto aos seus investimentos por conta propria.
