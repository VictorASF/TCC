import connectionDatabase as conn

# docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

#Metodo que cria uma tabela caso não exista
def criarTabela(nome):

    #Metodo do arquivo connectionDatabase.py que serve para se conectar ao banco de dados MySql
    database = conn.connectionDB()

    cursor = database.cursor()

    #Função que cria uma tabela caso a mesma não exista
    cursor.execute("CREATE TABLE IF NOT EXISTS "+ nome + """(
    id INT NOT NULL AUTO_INCREMENT,
    dia DATE NOT NULL,
    abertura DECIMAL(10,2) NOT NULL,
    fechamento DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id));""")
    database.commit()