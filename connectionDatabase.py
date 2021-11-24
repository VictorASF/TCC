import mysql.connector as my

# Método que cria uma conexão com o banco de dados


def connectionDB():
    database = my.connect(host='localhost',
                          database='readCSV',
                          user='root',
                          password='root',
                          port='3308')

    return database