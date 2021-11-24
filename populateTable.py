import pandas as pd
import os
import connectionDatabase as Conn
from createTable import criarTabela
from decimal import Decimal

# docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

# Conexão com o banco de dados
database = Conn.connectionDB()

# Variaveis que definem a localização do arquivo
user = os.getlogin()

path = f'C:/Users/{user}/Downloads/'
name_file = 'BTLG11'
type_file = 'csv'

# Variável que define o arquivo que será lido
file = f'{path}{name_file}.{type_file}'

# Variável que recebe a saida de uma função Pandas que lê o CSV
df = pd.read_csv(file)

cursor = database.cursor()

# Função do arquivo createTable.py que cria uma tabela a ser populada
criarTabela(name_file)

# Função que limpa a tabela caso a tabela já exista e tenha conteudo
# Essa limpeza é mais utilizada quando ocorre atualizações nos registros
cursor.execute('TRUNCATE FUNDOS.' + name_file + ';')
database.commit()


# Função for que popula a tabela de forma sequencial, utilizando somente da Data, do Valor de fechamento e de abertura
for num in range(df['Date'].size):
    dateFii = df['Date'][num]
    openFii = Decimal(df['Open'][num])
    closeFii = Decimal(df['Close'][num])
    cursor.execute('INSERT into FUNDOS.'+name_file+' (dia, abertura, fechamento) VALUES(%s,%s,%s)', (dateFii,
                                                                                                     openFii,
                                                                                                     closeFii))
    database.commit()

