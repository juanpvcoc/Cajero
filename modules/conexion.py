# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Conexión a la Base de Datos

# Módulo de mysql
from mysql import connector

mibanco = connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "mibancojpva2614986"
)