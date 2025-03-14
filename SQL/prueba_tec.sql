-- Primero creamos la base de datos para despues realizar la tabla necesaria, esta creacion es necesaria antes de crear la tabla en python aunque tambien se puede crear la base de datos en python
CREATE database prueba_tec;
-- Veamos si se ha creado correctamente
show databases;
-- Mostramos las tablas de la base de datos antes creada
show tables from prueba_tec;
select * from cargo;
-- Podemos usar la siguiente consulta para saber mas acerca de nuestra tabla
desc cargo;
select count(updated_at) from cargo;
