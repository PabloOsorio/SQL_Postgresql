PRUEBA PRACTICA PIPELINE

DESCRIPCION

Este proyecto implementa un data pipeline que automatiza el proceso de extracción, transformación y carga de datos desde un archivo CSV hacia bases de datos MySQL y PostgreSQL. El objetivo principal fue procesar un conjunto de datos en formato CSV, transformarlo según las necesidades y cargarlo en dos bases de datos diferentes para su posterior análisis y uso. Además se generó un diagrama de las tablas creadas en PostgreSQL y se creo una vista para facilitar consultas sobre las transacciones

OBJETIVOS DEL PROYECTO


Extracción: Leer los datos desde un archivo CSV y cargarlo en un DataFrame usando Python y librerias como pandas y numpy
Transformación: Limpiar los datos, renombrar columnas, realizar cambios en los tipos de datos y manejar valores nulos
Carga: Transferir los datos procesados a dos bases de datos distintas, MySQL y PostgreSQL

TECNOLOGIAS USADAS

Python: Usando bibliotecas como pandas y numpy para manipular los datos. Por otro lado mysql.connector para acceder a mysql y psycopg2 para acceder a Posgres estos ultimos de forma local
Excel: Se uso para dar un primer vistazo a las columnas y datos del csv
MySQL: Base de datos relacional utilizada para almacenar los datos y realizar consultas.
PostgreSQL: Otra base de datos relacional usada para almacenar y gestionar la información procesada, junto con la creación de una vista y un diagrama.
Git: Para la versión y el control de código


ACERCA DEL PROCESO

Extracción: 

Se utilizó pandas para cargar el archivo CSV. La estructura del CSV incluía columnas como id, company_id, amount, status, created_at, y paid_at, que representaban detalles de transacciones de diferentes compañías. Ademas con ayuda de excel buscamos valores repetidos y nulos por lo que pude averiguar a grandes rasgos los defectos en los datos a tomar en cuenta.

Transformación:

Renombrado de columnas: Se renombraron algunas columnas para mayor comodidad ya que se llamaria de igual forma en las tablas de las bases de datos
Limpieza de datos: Se corrigieron los valores nulos, se aseguraron los tipos de datos(por ejemplo, se transformó la columna amount a un tipo float y las fechas fueron convertidas al formato de fecha)
Eliminación de duplicados: Se eliminaron registros duplicados ya que si haciamos la carga en cualquier base de datos y habia un primary key duplicado nos daria errores.
Manejo de valores inconsistentes: Se manejaron valores nulos de forma que se les reemplaza por None


Carga:

MySQL: Se creó una tabla para almacenar los datos. Los datos procesados fueron cargados a la tabla de MySQL utilizando la librería pandas para insertar los datos directamente desde el DataFrame, se uso la funcion to_records para crear una lista de tuplas, donde cada tupla representa una fila del dataframe y con executemany se ejecuto la misma consulta sql varias veces con diferentes valores
PostgreSQL: Se creo una base de datos en PostgreSQL con dos tablas principales: companies (para almacenar la información de las compañías) y charges (para almacenar los detalles de las transacciones). Ademas se hizo una relación entre las tablas mediante claves foráneas. Por ultimo se generó una vista que permitía consultar el monto total transaccionado por día para las diferentes compañías y un diagrama con la misma ayuda del pgAdmin de posgres.


Conclusiones
Este proyecto proporcionó una solución para mover datos entre sistemas, automatizando tareas, garantizando la calidad de los datos y mejorando la velocidad de procesamiento. Además, se desarrollaron consultas en PostgreSQL para facilitar el análisis de los datos, y el uso de ETL permitió transformar datos crudos en información útil y bien estructurada. Como experiencia personal me llevo la importancia de limpiar los datos y revisar las distintas problematicas que puedan traer, ya sean formatos, nulos, tipos de dato, duplicados y outliners. Por otra lado aprendi mas acerca de postgresql y MySQL asi como sus diferencias y beneficios. 
El por que elegi llevar todo el proceso en MySQl y Postgres (bases de datos relacionales y estructuradas) es porque vi la necesidad de mantener los datos organizados y crear relaciones entre las tablas lo que despues me permitiria poder manipularlos de manera logica. 

