import pandas as pd
import connectionDatabase as conn


database = conn.connectionDB()

cursor = database.cursor()

cod_fii = 'HGLG11'

#TRATAR FUNDOS KNRI11, E HFOF11

dia_inicio = '2017-01-01'

dia_fim = '2021-08-09'


#cursor.execute('SELECT count(fechamento) from '+cod_fii+' WHERE dia >="'+dia_inicio+'" and dia <="'+dia_fim+'";')
#N = cursor.fetchone()
#N = (N[0])

#Select no banco para pegar os valores de abertura do fundo nos dias indicados
cursor.execute('SELECT dia, fechamento from '+cod_fii+' WHERE dia >="'+dia_inicio+'" and dia <="'+dia_fim+'";')
fii = cursor.fetchall()

#Select no banco para pegar o valor de abertura do IFIX(benchmark) nos dias indicados
cursor.execute('SELECT dia, fechamento from IFIX WHERE dia >="'+dia_inicio+'" and dia <="'+dia_fim+'";')
ifix= cursor.fetchall()

cursor.execute('SELECT dia from IFIX WHERE dia >="'+dia_inicio+'" and dia <="'+dia_fim+'";')
dias= cursor.fetchall()

#Variavel auxiliar para limpar qualquer dia incluso onde a bolsa não funcionou
dia_auxiliar = []


#For para atribuir o dia da lista
for dia in ifix:
    dia_auxiliar.append(dia[0])

#For que faz a comparação e exclusão de dias desnecessarios para não causar erro no calculo futuro
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

for i in range(len(dias)-1):
    if i+1 < len(dias):
        vet_return_ifix.append(1 - (vet_ifix[i]/vet_ifix[i+1]))

for i in range(len(dias) - 1):
    if i + 1 < len(dias):
        vet_return_fii.append(1 - (vet_fii[i] / vet_fii[i + 1]))

media_return_fii = 0
media_return_ifix = 0

for x in vet_return_ifix:
    media_return_ifix += x
media_return_ifix = media_return_ifix/(len(vet_return_ifix))

for x in vet_return_fii:
    media_return_fii += x
media_return_fii = media_return_fii/(len(vet_return_fii))

print(f"Retorno media FII: {media_return_fii}")
print(f"Retorno media IFIX: {media_return_ifix}")

COV = 0
VAR = 0

for x in range(len(vet_return_fii)):
    COV += ((vet_return_fii[x]-media_return_fii)*(vet_return_ifix[x]-media_return_ifix))
COV = COV/(len(vet_return_fii))

print(f"Covariancia: {COV}")

for x in range(len(vet_return_ifix)):
    VAR += (vet_return_ifix[x]-media_return_ifix)**2
VAR = VAR/(len(vet_return_ifix)-1)

print(f"Variancia: {VAR}")

Beta = COV/VAR
Beta = float(Beta)

print(f"Indice Beta: {Beta}")