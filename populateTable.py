import pandas as pd
import connectionDatabase as conn
from createTable import criarTabela
from decimal import Decimal
from datetime import datetime

# docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

#Conexão com o banco de dados
database = conn.connectionDB()

#Variaveis que definem a localização do arquivo

path = 'C:/Users/vfonseca/Downloads/'
name_file = 'MXRF11'
#name_file = 'Índice de Fundos de Investimentos Imobiliários (IFIX) - Histórico  InfoMoney'
type_file = 'csv'

#Variavel que define o arquivo que será lido

file = f'{path}{name_file}.{type_file}'

#Variavel que recebe a saida de uma função Pandas que lê o CSV

df = pd.read_csv(file)

#print(df[['Date', 'Open']].to_string(index=False))

cursor = database.cursor()

#Função do arquivo createTable.py que cria uma tabela a ser populada
criarTabela(name_file)

#Função que limpa a tabela caso a tabela já exista e tenha conteudo
#Essa limpeza é mais utilizada quando ocorre atualizações nos registros
cursor.execute('TRUNCATE '+name_file+';')
database.commit()


#Função for que popula a tabela de forma sequencial, utilizando somente da Data, do Valor de fechamento e de abertura
for num in range(df['Date'].size):
    dateFii = df['Date'][num]
    if num == 0:
        openFii = Decimal(df['Close'][num])
    else:
        openFii = Decimal(df['Close'][num-1])
    closeFii = Decimal(df['Close'][num])
    cursor.execute('INSERT into readCSV.'+name_file+' (dia, abertura, fechamento) VALUES(%s,%s,%s)', (dateFii,
                                                                                                       openFii,
                                                                                                       closeFii))
    database.commit()

print('IHUUUUUU, importação na tabela '+name_file+' realizada com sucesso!')

