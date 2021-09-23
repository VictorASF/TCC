import connectionDatabase as Conn


# docker run --name=Mysql56 -e MYSQL_ROOT_PASSWORD=root -p 3308:3306 -d mysql:5.6

# Metodo que cria uma tabela caso não exista


def criarTabela(nome):
    # Metodo do arquivo connectionDatabase.py que serve para se conectar ao banco de dados MySql
    database = Conn.connectionDB()

    cursor = database.cursor()

    # Função que cria uma tabela caso a mesma não exista
    cursor.execute("CREATE TABLE IF NOT EXISTS " + nome + """(
    id INT NOT NULL AUTO_INCREMENT,
    dia DATE NOT NULL,
    abertura DECIMAL(10,2) NOT NULL,
    fechamento DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id));""")
    database.commit()


def criarTabelaDividendo(nome):
    database = Conn.connectionDB()

    cursor = database.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS dividend." + nome + """(
    id INT NOT NULL AUTO_INCREMENT,
    mes DATE NOT NULL,
    yield FLOAT NOT NULL,
    PRIMARY KEY (id));""")
