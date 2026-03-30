# apis
Creacion de API's

# Aplicacion 000
1. Primero instalas fastapi[standard]
2. EL coidgo de partida es de fast api
3. Para ver la documentacion al finalizar de la url simplemnete pones /docs 

# Aplicacion 001
1. Hacer una agenda, en este caso con sqlite3 con estos parametros  
  
|  Contactos    |              | 
|:-------------:|:------------:|
| id_contacto   | int PK       |
| nombre        | varchar (100)|
|email          | varchar (100)|
|telefono       | varchar (100)|  

Insertar 100 registros

2. Hacer un /docs  

| No.      | Propiedad| Detalle  |
|----------|----------|:----------:|
|1| Description|Endpoint de Bienvenida|
|2| Summary|Endpoint de BIenvenida a la agenda|
|3| Method|GET|
|4| Endpoint|/|
|5| Authentication|NA|
|6| Query param|NA|
|7| Path param|NA|
|8| Data|NA|
|9| Status Code|202|
|10| Response|{"message":"Agenda", "datetime": "timestamp"}|
|11| Response Type|application/json|
|12| Status Code (error)|NA|
|13| Response Type(error) |NA|
|14| Response (error)|NA|
|15| cURL|curl -X GET http://127.0.0.1:8000/|

3. Consultar todos los contactos  

| No.      | Propiedad| Detalle  |
|----------|----------|:----------:|
|1| Description|Endpoint para consultar todos los contactos|
|2| Summary|Regresa los contactos paginados|
|3| Method|GET|
|4| Endpoint|/v1/contactos|
|5| Authentication|NA|
|6| Query param|limit:int&skip:int|
|7| Path param|NA|
|8| Data|NA|
|9| Status Code|202|
|10| Response|{"table":"contactos", "items": [{"id_contacto":int, "nombre": str,"email": str, "telefono": str}],"count":int, "datetime": timestamp, "message":"Datos consultados exitosamente",limit":10,"skip":0}|
|11| Response Type|application/json|
|12| Status Code (error)|400, 401, 403, 404, 409, 422, 500, 501, 502, 503, 504|
|13| Response Type(error) |applicaction/json|
|14| Response (error)|{"detail":"Parámetros inválidos", "datetime":"timestamp"} / {"detail":"Direccion Incorrecta", "datetime":"timestamp"} / {"detail":"No puedes entrar Acceso prohibido", "datetime":"timestamp"} / {"detail":"No se encontraron contactos", "datetime":"timestamp"} / {"detail":"Conflicto: contacto duplicado", "datetime":"timestamp"}|
|15| cURL|curl -X GET http://127.0.0.1:8000/|


4. Buscar Contactos  

| No.      | Propiedad| Detalle  |
|----------|----------|:----------:|
|1| Description|Endpoint para buscar un contacto|
|2| Summary|Regresa el contacto buscado|
|3| Method|GET|
|4| Endpoint|/v1/contactos/{id_contacto}|
|5| Authentication|NA|
|6| Query param|NA|
|7| Path param|id_contacto:int|
|8| Data|NA|
|9| Status Code|202|
|10| Response|{"table":"contactos", "items":[{"id_contacto":int, "nombre": str,"email": str, "telefono": str}],"count":int,"datetime": timestamp, "message":"Datos consultados exitosamente"}|
|11| Response Type|application/json|
|12| Status Code (error)|400|
|13| Response Type(error) |application/json|
|14| Response (error)|{"table": "contactos","item": {},"count": 0, "datetime": timestamp, "message": "este contacto no existe"} / {"detail":"Error al buscar el registro", "datetime":"timestamp"}|
|15| cURL|curl -X GET http://127.0.0.1:8000/v1/contactos/3|  


5. Insertar contacto  

| No.      | Propiedad| Detalle  |
|----------|----------|:----------:|
|1| Description|Endpoint para insertar un contacto|
|2| Summary|Inserta un contacto validando campos|
|3| Method|POST|
|4| Endpoint|/v1/contactos|
|5| Authentication|NA|
|6| Query param|NA|
|7| Path param|NA|
|8| Data|{"nombre": str, "email": str, "telefono": str}|
|9| Status Code|201|
|10| Response|{"table":"contactos", "item": {"id_contacto":int, "nombre": str, "email": str, "telefono": str}, "datetime": timestamp, "message":"Contacto insertado exitosamente"}|
|11| Response Type|application/json|
|12| Status Code (error)|400|
|13| Response Type(error) |application/json|
|14| Response (error)|{"detail":"Error en la base de datos", "datetime":"timestamp"} / {"message":"Campos vacios", "datetime":"timestamp"}|
|15| cURL|curl -X POST http://127.0.0.1:8000/v1/contactos -H "Content-Type: application/json" -d '{"nombre":"Liz", "email":"liz@email.com", "telefono":"1234567890"}'|

6. Modificar contacto  

| No.      | Propiedad | Detalle |
|----------|-----------|:-------:|
|1| Description|Endpoint para modificar un contacto por id|
|2| Summary|Actualiza nombre, email y telefono de un contacto|
|3| Version|v1|
|4| Method|PUT|
|5| Endpoint|/v1/contacto|
|6| Authentication|NA|
|7| Query param|id_contacto:int|
|8| Path param|NA|
|9| Data|{"nombre": str, "email": str, "telefono": str}|
|10| Status code|202|
|11| Response type|application/json|
|12| Response|{"table":"contactos", "item": {"id_contacto":int, "nombre": str, "email": str, "telefono": str}, "count":1, "datetime": timestamp, "message":"Contacto actualizado exitosamente"}|
|13| Status code (error)|400, 401, 404|
|14| Response type (error)|application/json|
|15| Response (error)|{"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"El id no puede ser negativo"} / {"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"Campos vacios"} / {"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"El email debe contener @"} / {"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"este contacto no existe"} / {"detail":"Error al actualizar el registro", "datetime":"timestamp"}|
|16| cURL|curl -X PUT "http://127.0.0.1:8000/v1/contacto?id_contacto=3" -H "Content-Type: application/json" -d '{"nombre":"Liz Actualizada", "email":"liz.actualizada@email.com", "telefono":"1234567890"}'|
|17| Table|contactos|

7. Eliminar contacto  

| No.      | Propiedad | Detalle |
|----------|-----------|:-------:|
|1| Description|Endpoint para eliminar un contacto por id|
|2| Summary|Elimina un contacto existente de la tabla contactos|
|3| Version|v1|
|4| Method|DELETE|
|5| Endpoint|/v1/contacto|
|6| Authentication|NA|
|7| Query param|id_contacto:int|
|8| Path param|NA|
|9| Data|NA|
|10| Status code|202|
|11| Response type|application/json|
|12| Response|{"table":"contactos", "item": {"id_contacto":int, "nombre": str, "email": str, "telefono": str}, "count":1, "datetime": timestamp, "message":"Contacto eliminado exitosamente"}|
|13| Status code (error)|400, 404|
|14| Response type (error)|application/json|
|15| Response (error)|{"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"el campo no puede estar vacio"} / {"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"El id no puede ser negativo"} / {"table":"contactos", "item":{}, "count":0, "datetime": timestamp, "message":"este contacto no existe"} / {"detail":"Error al eliminar el registro", "datetime":"timestamp"}|
|16| cURL|curl -X DELETE "http://127.0.0.1:8000/v1/contacto?id_contacto=3"|
|17| Table|contactos|

