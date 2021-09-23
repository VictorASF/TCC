import connectionDatabase as Conn

database = Conn.connectionDB()

cursor = database.cursor()

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

valor_investido = 10000

dia_inicio = '2017-01-01'

dia_fim = '2021-09-06'

# Select no banco para pegar os valores de abertura do fundo nos dias indicados
cursor.execute(
    'SELECT dia, fechamento from readCSV.' + cod_fii + ' WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
fii = cursor.fetchall()

# Select no banco para pegar o valor de abertura do IFIX(benchmark) nos dias indicados
cursor.execute('SELECT dia, fechamento from readCSV.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
ifix = cursor.fetchall()

cursor.execute('SELECT dia from readCSV.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
dias = cursor.fetchall()

cursor.execute('SELECT count(dia) from readCSV.IFIX WHERE dia >="' + dia_inicio + '" and dia <="' + dia_fim + '";')
contador = cursor.fetchall()
contador = (contador[0][0])

cursor.execute('SELECT timestampdiff(MONTH,"' + dia_inicio + '", "' + dia_fim + '") from readCSV.IFIX;')
meses = cursor.fetchall()
meses = (meses[0][0])

cursor.execute(
    'SELECT yield from dividend.' + cod_fii + ' WHERE mes >="' + dia_inicio + '" and mes <="' + dia_fim + '";')

yieldList = cursor.fetchall()

sumYield = 0

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

vet_dia = []
vet_ifix = []
vet_fii = []

for dia in dias:
    vet_dia.append(dia[0])
for x in ifix:
    vet_ifix.append(x[1])
for x in fii:
    vet_fii.append(x[1])

vet_ifix.reverse()
vet_fii.reverse()

vet_return_ifix = []
vet_return_fii = []
vet_preco_medio = 0

for i in range(len(dias) - 1):
    if i + 1 < len(dias):
        vet_return_ifix.append(1 - (vet_ifix[i] / vet_ifix[i + 1]))

for i in range(len(dias) - 1):
    if i + 1 < len(dias):
        vet_return_fii.append(1 - (vet_fii[i] / vet_fii[i + 1]))

for i in range(len(dias) - 1):
        vet_preco_medio += vet_fii[i]

vet_preco_medio = float(vet_preco_medio/len(dias))

media_return_fii = 0
media_return_ifix = 0

for x in vet_return_ifix:
    media_return_ifix += x
media_return_ifix = media_return_ifix / (len(vet_return_ifix))

for x in vet_return_fii:
    media_return_fii += x
media_return_fii = media_return_fii / (len(vet_return_fii))

# print(f"Retorno media FII: {media_return_fii}")
# print(f"Retorno media IFIX: {media_return_ifix}")

COV = 0
VAR = 0

for x in range(len(vet_return_fii)):
    COV += ((vet_return_fii[x] - media_return_fii) * (vet_return_ifix[x] - media_return_ifix))
COV = COV / (len(vet_return_fii))

# print(f"Covariancia: {COV}")

for x in range(len(vet_return_ifix)):
    VAR += (vet_return_ifix[x] - media_return_ifix) ** 2
VAR = VAR / (len(vet_return_ifix) - 1)

# print(f"Variancia: {VAR}")

Beta = COV / VAR
Beta = float(Beta)

print(f"Indice Beta {cod_fii}: {Beta:0.4f}")

# Retorno calculo do retorno IFIX
retorno_ifix = ((vet_ifix[0] / vet_ifix[len(vet_ifix) - 1]) - 1)

# Retorno calculo de retorno FII onde o primeiro valor do FII é dividido pelo ultimo valor -1
# e esse resultado é subtraido 1

retorno_fii = ((vet_fii[0] / vet_fii[len(vet_fii) - 1]) - 1)

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
cotas = float(valor_investido//vet_fii[-1])
rendimentos = float((sumYield/100)*vet_preco_medio)
print(f'No ato da compra geraria {cotas} cotas que renderam cada cota {rendimentos:0.2f}')
print(f'Ou R${cotas*rendimentos:0.2f} no total')


