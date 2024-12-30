from tkinter import messagebox
import oracledb as ora


def obtener_conexion():
    try:
        #Parámetros de conexión
        host = "DESKTOP-FRJS6KI"
        puerto = 1521 
        nombre_servicio = "XE" 
        usuario = "SYSTEM" 
        password = "Ragnar7m7.,-" 
        #string de conexión
        dsn = f"{host}:{puerto}/{nombre_servicio}"
        connection = ora.connect(user=usuario, password=password, dsn=dsn)

    except ora.DatabaseError as e:
        messagebox.showwarning("Error",f"Error en la conexión o en la consulta: {e}")

    return connection

def obtener_cursor():   
    #Obtiene un cursor a partir de una conexion
    connection = obtener_conexion()
    return connection.cursor(), connection

