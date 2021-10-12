import pandas as pd
import os
import connectionDatabase as Conn
from createTable import criarTabela
from decimal import Decimal

# docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

# Conexão com o banco de dados
database = Conn.connectionDB()

user = os.getlogin()

path = f'C:/Users/{user}/Downloads/'
name_file = 'IFIX'
# name_file = 'Índice de Fundos de Investimentos Imobiliários (IFIX) - Histórico  InfoMoney'
type_file = 'txt'

file = f'{path}{name_file}.{type_file}'


df = pd.read_csv(file, sep='\t', encoding='utf-16')

df['Date'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df['Date'] = df['Date'].dt.strftime('%y-%m-%d')
df['Close'] = df['Valor'].apply(Decimal)

# print(df[['Date', 'Open']].to_string(index=False))
cursor = database.cursor()

criarTabela(name_file)

cursor.execute('TRUNCATE FUNDOS.'+name_file+';')
database.commit()

for num in range(df['Date'].size):
    dateFii = df['Date'][num]
    if num == 0:
        openFii = df['Close'][num]
    else:
        openFii = df['Close'][num-1]
    closeFii = df['Close'][num]
    cursor.execute('INSERT into FUNDOS.'+name_file+' (dia, abertura, fechamento) VALUES(%s,%s,%s)', (dateFii,
                                                                                                     openFii,
                                                                                                     closeFii))
    database.commit()

print('IHUUUUUU, importação na tabela '+name_file+' realizada com sucesso!')


