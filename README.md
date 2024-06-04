# Ferremas
Una api en base a un proyecto del instituto DUOC y el cual se tiene planeado crear una app para gestionar productos de una ferreteria.

MongoDB = https://www.mongodb.com/

# Comandos
Activar entorno virtual = .\venv\Scripts\activate

# Postman Usuarios
Crear Usuario
http://127.0.0.1:5000/api/ferremas/createuser
Ejemplo:
{
    "username": "Manu",
    "password": "1234"
}

Login Usuario
http://127.0.0.1:5000/api/ferremas/login
{
    "username": "Manu",
    "password": "1234"
}

Login Admin con token de acceso correspondiente
http://127.0.0.1:5000/api/ferremas/createadmin
{
    "username": "Manu",
    "password": "1234"
}

Listar todos los usuarios, solo admins
http://127.0.0.1:5000/api/ferremas/viewuser

Eliminar usuario, solo admins
http://127.0.0.1:5000/api/ferremas/deleteuser/<user_id>

# Postman Productos