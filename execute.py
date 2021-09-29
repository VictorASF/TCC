import connectionDatabase as Conn
from matplotlib import pyplot as matt
import numpy as nump

# Variavel que gera a conexão com o banco de dados
database = Conn.connectionDB()

# Variavel usada para executar funções no banco como SELECT, TRUNCATE, DELETE
cursor = database.cursor()

# Variavel que recebe o fundo que será utilizado para efetuar os calculos
cod_fii = 'BTLG11'

# Opções de FII
# BTLG11 Imovel Logistico
# BRCR11 Lajes Corporativas
# HGBS11 Shoppings
# HGLG11 Imovel Logisticos
# HGRE11 Lajes Corporativas
# KNRI11 Misto
# MXRF11 Papéis
# VRTA11 Papéis
# BBPO11 Agencias Bancarias
# MFII11 Fundo de Desenvolvimento
# BPFF11 Fundo de Fundos

# Variavel que é usada de exemplo para definir valores dos rendimentos
valor_investido = 10000

# Variavel de dia inicial que vai determinar o inicio do periodo no banco de dados
dia_inicio = '2017-01-01'

# Variavel do dia final que vai determinar o fim do periodo que deve ser buscado no banco
dia_fim = '2021-09-06'
#dia_fim = '2021-09-06'

# Select no banco para selecionar os valores de abertura do fundo nos dias indicados
cursor.execute(
    'SELECT dia, fechamento from FUNDOS.' + cod_fii + ' WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
fii = cursor.fetchall()

# Select no banco para selecionar o valor de fechamento do IFIX(benchmark) nos dias indicados
cursor.execute('SELECT dia, fechamento from FUNDOS.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
ifix = cursor.fetchall()

# Select no banco para selecionar os dias que a bolsa funcionou
cursor.execute('SELECT dia from FUNDOS.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
dias = cursor.fetchall()

# Select no banco para selecionar a quantidade de dias que a bolsa funcionou
# cursor.execute('SELECT count(dia) from readCSV.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
# contador_dia = cursor.fetchall()
# contador_dia = (contador_dia[0][0])

# Select no banco que vai definir a quantidade de meses existentes no periodo selecionado
cursor.execute('SELECT timestampdiff(MONTH,"' + dia_inicio + '", "' + dia_fim + '") from FUNDOS.IFIX;')
meses = cursor.fetchall()
meses = (meses[0][0])

# Select do Dividend Yield mensal definido pelo dia_inicio e dia_fim
cursor.execute(
    'SELECT yield from DIVIDENDOS.' + cod_fii + ' WHERE mes >="' + dia_inicio + '" and mes <="' + dia_fim + '";')
yieldList = cursor.fetchall()

sumYield = 0

# For utilizado para fazer a soma do dividend yield antes numa lista em uma variavel tipo float
for i in yieldList:
    sumYield += i[0]

# Variavel auxiliar para limpar qualquer dia incluso onde a bolsa não funcionou
dia_auxiliar = []

# For para atribuir o dia da lista
for dia in ifix:
    dia_auxiliar.append(dia[0])

# For que faz a comparação e exclusão de dias desnecessarios para não causar erro no calculo futuro
for dia in fii:
    if dia[0] not in dia_auxiliar:
        fii.remove(dia)


# Variaveis auxiliares para filtrar os valores que foram coletados do banco
list_dia = []
list_ifix = []
list_fii = []

# For utilizado para receber a data do pregão que foi removida do banco,
# como a variavel dias é uma lista de tuplas com 2 valores cada é necessario filtrar só o primeiro valor
# que é o valor que realmente interessa
for dia in dias:
    list_dia.append(dia[0])

# Os 2 for abaixo são usados com a mesma finalidade pegar os valores de fechamento do IFIX e FII
# (IFIX para o primeiro for, FII para o segundo for)
for x in ifix:
    list_ifix.append(x[1])
for x in fii:
    list_fii.append(x[1])

# Como os valores estão ordenados de forma crescente no periodo de dias é preciso inverter os valores para que na
# posição 0 fique o valor mais recente e na posição x+1 vá ficando o valor mais antigo
list_ifix.reverse()
list_fii.reverse()
list_dia.reverse()

# Variaveis de apoio que irão receber respectivamente o retorno do Benchmark, do Fundo
# e a soma total do preço diario do fundo
list_return_ifix = []
list_return_fii = []
list_return_dia = []
preco_medio = 0

# Os 2 For utilizados abaixo são para saber se a divisão do dia i com o dia anterior é maior ou menor que 1
# sendo maior que 1 significa que o valor do dia mais atual é maior que o mais antigo e menor que o valor atual é
# menor que o dia anterior
for i in range(len(dias) - 1):
    list_return_ifix.append((list_ifix[i] / list_ifix[i + 1])-1)

for i in range(len(dias) - 1):
    list_return_fii.append((list_fii[i] / list_fii[i + 1])-1)

# For que soma os valores diarios de fechamento para que futaramente possa ser dividido a fim de achar um preço medio
for i in range(len(dias) - 1):
    preco_medio += list_fii[i]

for i in range(len(dias) - 1):
    list_return_dia.append(list_dia[i])

# Variavel agora recebendo a divisão em float do total do preco_medio pelo quantidade de dias de pregão
preco_medio = float(preco_medio/len(dias))

# Variaveis que receberam a media dos retornos efetivos dos FII e o IFIX em valorização ou desvalorizção
media_return_fii = 0
media_return_ifix = 0

# For executando a soma de todos os valores existentes nas listas de retorno e ao fim executando uma divisão
# pela quantidade de pregões
for x in list_return_ifix:
    media_return_ifix += x
media_return_ifix = media_return_ifix / (len(list_return_ifix))

print(media_return_ifix)

for x in list_return_fii:
    media_return_fii += x
media_return_fii = media_return_fii / (len(list_return_fii))

print(media_return_fii)

# Variaveis definidas para executar o calculo do Indice Beta
COV = 0
VAR = 0

# Covariancia é um for que recebe como range o tamanho da lista que será executada, onde a Covariancia final é
# o somatorio de todas essa operação e isso realiza
# subtraindo do valor de retorno do ativo a ser analisado com a media de retorno desse valor
# e isso se multiplica pelo valor de retorno do benchmark subtraido da media de retorno desse benchmark
# onde para que isso aconteça esses valores precisam ser do mesmo dia
# ao fim do somatorio a covariancia total é dividida pelo tamanho da lista chegando assim ao resultado final
for x in range(len(list_return_fii)):
    COV += ((list_return_fii[x] - media_return_fii) * (list_return_ifix[x] - media_return_ifix))
COV = COV / (len(list_return_fii))

# Variancia é um for que recebe o tamanho de uma lista como range e executa um somatorio da
# subtração do retorno do benchmark ao quadrado e ao fim é executado a divisão da variancia somada com o resultado final
for x in range(len(list_return_ifix)):
    VAR += (list_return_ifix[x] - media_return_ifix) ** 2
VAR = VAR / (len(list_return_ifix) - 1)

# Calculo de Beta onde é Covariancia/Variancia
Beta = float(COV / VAR)

print(f"Indice Beta {cod_fii}: {Beta:0.4f}")

# Retorno calculo do retorno IFIX
retorno_ifix = ((list_ifix[0] / list_ifix[len(list_ifix) - 1]) - 1)

# Retorno calculo de retorno FII onde o primeiro valor do FII é dividido pelo ultimo valor -1
# e esse resultado é subtraido 1

retorno_fii = ((list_fii[0] / list_fii[len(list_fii) - 1]) - 1)

# CAPM

returnFreeOfRisk = (5.25 / 100)

returnBenchmark = float(retorno_ifix)

returnExpected = returnFreeOfRisk + (Beta * (returnBenchmark - returnFreeOfRisk))
print(f'Retorno Esperado (CAPM) do FII {cod_fii}: {returnExpected * 100:05.2f}%')
print(f'Retorno IFIX: {retorno_ifix * 100:05.2f}%')
print(f'Retorno real do FII {cod_fii}: {retorno_fii * 100:05.2f}%')
print(
    f'Retorno sobre um investimento de R${valor_investido}: R${valor_investido + (retorno_fii * valor_investido):0.2f}')

print(f'Retorno em redimentos {cod_fii} com o valor de R${valor_investido} investido:')

# Dividendos
cotas = float(valor_investido//list_fii[-1])
rendimentos = float((sumYield/100)*preco_medio)
print(f'No ato da compra geraria {cotas} cotas que renderam cada cota {rendimentos:0.2f}')
print(f'Ou R${cotas*rendimentos:0.2f} no total')


"""matt.plot(list_return_dia, list_return_ifix)
matt.plot(list_return_dia, list_return_fii, ':')
matt.title(f'Retorno Diario {cod_fii} x IFIX periodo {dia_inicio} a {dia_fim}')
matt.xlabel('Periodo')
matt.ylabel('Retorno (%)')
matt.legend(['IFIX', cod_fii])
matt.grid()
matt.show()
"""
x = nump.array(list_return_ifix)
y = nump.array(list_return_fii)
x = (nump.float_(x))
y = (nump.float_(y))

matt.plot(x,y, 'o')

m, b = nump.polyfit(x, y, 1)

matt.plot(x, m*x + b)
matt.title(f'Beta {cod_fii} periodo {dia_inicio} a {dia_fim}')
matt.xlabel('IFIX')
matt.ylabel(cod_fii)
matt.grid()
matt.show()

