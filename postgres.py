import psycopg2
import pandas as pd
import numpy as np


#Ahora nos comunicaremos cons postgres
conn = psycopg2.connect(
    dbname="prueba_tec",
    user = "postgres",
    password = "Camaleon69",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

#Mostremos las bases de datos existentes
cursor.execute("SELECT datname FROM pg_database;")
databases = cursor.fetchall()#Hace tuplas
for database in databases:
    print(database[0])  # Imprime solo el nombre de la base de datos



#Empecemos con la creacion de la tabla companies
cursor.execute("""
Create table if not exists companies (
    company_id varchar(50) PRIMARY KEY,
    company_name VARCHAR(130) NOT NULL
);
""")

#Ahora la creacion de la tabla charges y su relacion con companies
cursor.execute("""
CREATE TABLE IF NOT EXISTS charges(
    id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50),
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);
""")
conn.commit()#Guardamos cambios

#Limpiemos y acomodemos el CSV
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
    #Manejar nulos en las fechas
    df["created_at"] = df["created_at"].apply(lambda x: None if pd.isnull(x) else x)
    df["updated_at"] = df["updated_at"].apply(lambda x: None if pd.isnull(x) else x)

    return df

def insert_data_to_postgres(df,conn):
    cursor = conn.cursor()

    #Buscamos primero los valores unicos de nuestra columna company_id
    unique_company_ids = df["company_id"].unique()

    #Insertamos solo los unicos
    for company_id in unique_company_ids:
    #Filtramos para obtener el nombre de la empresa
        filtered_df = df[df["company_id"] == company_id]

        if not filtered_df.empty:
            company_name = filtered_df["company_name"].iloc[0]  # Buscar el nombre de la empresa
        else:
            company_name = "Desconocido" 


        cursor.execute("""
        Insert into companies(company_id,company_name)
        VALUES(%s,%s)
        ON CONFLICT (company_id) DO NOTHING
        """, (company_id, company_name))
    
    #Ahora a insertar las transacciones
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO charges(id, company_id, amount, status, created_at, updated_at)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,(row["id"], row["company_id"], row["amount"], row["status"],row["created_at"],row["updated_at"]))

    conn.commit()#Guardamos cambios
    cursor.close()


file_path = r"C:\Users\pablo\Documents\VisualS\data_prueba.csv"
df = pd.read_csv(file_path)  # Carga los datos

print(df.head())  # Verifica que los datos se cargaron correctamente


#Preprocesar
df = preprocess_data(df)

# Llama a la función con la conexión a PostgreSQL
insert_data_to_postgres(df, conn)

conn.close()

