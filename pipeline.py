import pandas as pd
import mysql.connector
import numpy as np
import os

#Funcion para establecer conexion con mysql
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Camaleon69",
            database = "prueba_tec"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a mysql: {err}")
        return None
    
#funcion para la creacion de la tabla    
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    Create table if not exists Cargo (
        id VARCHAR(50) not NULL,
        company_name VARCHAR(130) NULL,
        company_id VARCHAR(50) NOT NULL,
        amount DECIMAL(16,2) NOT NULL,
        status VARCHAR(30) NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NULL,
        PRIMARY KEY (id)

    )
""")
    conn.commit
    cursor.close()

def load_data(file_path):
    df = pd.read_csv(file_path)
    print("Datos cargados")
    return df

def preprocess_data(df):
    df.rename(columns={
        "id":"id",
        "name":"company_name",
        "company_id":"company_id",
        "amount":"amount",
        "status":"status",
        "created_at":"created_at",
        "paid_at":"updated_at",
    }, inplace=True)
    #Sigamos con la modificacion de las columnas, tipos, duplicados, nulos
    df["id"] = df["id"].astype(str)
    df["id"] = df["id"].fillna(df["id"].apply(lambda x: f"unique_{np.random.randint(100000,999999)}"))
    #Eliminar duplicados
    df.drop_duplicates(subset=["id"], inplace = True)
    #Convertir columnas al type correcto
    df["company_name"] = df["company_name"].astype(str)
    df["company_id"] = df["company_id"].astype(str)
    df["status"] = df["status"].astype(str)
    df["amount"] = df["amount"].astype(float)
    df["amount"] = df["amount"].apply(lambda x: min(x, 999999999) if x > 0 else 0)

    df["created_at"] = df["created_at"].apply(lambda x: None if pd.isnull(x) else x)
    df["updated_at"] = df["updated_at"].apply(lambda x: None if pd.isnull(x) else x)

    return df

def insert_data_to_mysql(df,conn):
    cursor = conn.cursor()
    sql = """
    INSERT INTO cargo (id, company_name, company_id, amount, status, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = df.to_records(index=False).tolist()
    cursor.executemany(sql, data)
    conn.commit()
    print("Datos insertados")
    cursor.close()

def main():
    file_path = r"C:\Users\pablo\Documents\VisualS\data_prueba.csv"
    conn = connect_to_mysql()
    if conn:
        create_table(conn)
        df = load_data(file_path)
        df = preprocess_data(df)
        insert_data_to_mysql(df, conn)
        conn.close()
        print("Pipeline exitoso")

if __name__=="__main__":
    main()