import mysql.connector
from credentials import usr, pswd

def insert_db(value1, value2, value3, value4, value5, value6):
    try:  
        mydb = mysql.connector.connect(
            host = "localhost",
            user = usr,
            password = pswd,
            database = "dbOverall"
        )

        if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Conectado ao MySQL Server versão ", db_Info)

            mycursor = mydb.cursor()

            sql_query = "INSERT INTO tblDadosServidor(dataHora, cpu, memoria, disco, processosAtivos, usuarioAtual, fkServidor) VALUES (now(),%s,%s,%s,%s,%s,%s)"
            val = [value1, value2, value3, value4, value5, value6]
            mycursor.execute(sql_query, val)

            mydb.commit()

            print(mycursor.rowcount, "registro inserido")
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("Conexão com MySQL está fechada\n")
