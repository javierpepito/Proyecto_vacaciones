from Conexion import *


class Personaje():
    def __init__(self,nombre,nivel,salud,experiencia,arma=None): 
        self.nombre = nombre
        self.nivel = nivel
        self.salud = salud
        self.experiencia = experiencia
        self.arma = arma

    def __str__(self):
        return F"nombre: {self.nombre}, nivel: {self.nivel}, salud: {self.salud}, experiencia: {self.experiencia}"

    def crear_personaje(self):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""INSERT INTO personaje (id, nombre, nivel, salud, experiencia) VALUES (seq_id_personaje.nextval, :1, :2, :3, :4)""", (self.nombre, self.nivel, self.salud, self.experiencia))    
            connection.commit()
            messagebox.showinfo("",F"Se a realizado la insersión del personaje: {self.nombre}.")
        except Exception as e:
            messagebox.showwarning("",F"No se pudo realizar la inserción del personaje: {self.nombre}. ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def asignar_arma_personaje(self,id_personaje,municion_disponible,id_arma):
        try:
            cursor, connection = obtener_cursor()
            self.arma = id_arma
            cursor.execute(""" INSERT INTO arma_personaje (id_relacion,municiones_disponibles,personaje_FK,arma_FK) values (seq_id_intermedia.nextval, :1, :2, :3)""",(municion_disponible, id_personaje, self.arma))
            connection.commit()
            messagebox.showinfo("",F"Se a agregado correctamente el arma con id: {self.arma} a el personaje llamado: {self.nombre}.")
        except Exception as e:
            messagebox.showwarning("",F"No se pudo realizar la asignacion del arma con id: {self.arma} al personaje: {self.nombre}. ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def quitar_arma_personaje(self,id_personaje,id_arma):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""DELETE FROM arma_personaje where personaje_FK = :1 AND arma_FK = :2""",(id_personaje,id_arma))
            connection.commit()
            messagebox.showinfo("",F"Se ha eliminado el arma con id: {id_arma} del personaje llamado: {self.nombre}.")
        except Exception as e:
            messagebox.showwarning("",F"No se pudo elimar el arma con id: {id_arma} del personaje: {self.nombre}. ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def aumentar_nivel(self,id_ingresado,nivel_actualizado):
        try:
            cursor, connection = obtener_cursor()
            self.nivel += nivel_actualizado
            cursor.execute("""update personaje set nivel = :1 where id = :2""", (self.nivel,id_ingresado))    
            connection.commit()
            messagebox.showinfo("",F"Se ha actualizado el nivel del personaje: {self.nombre} ha aumentado {nivel_actualizado} de nivel, ahora tiene {self.nivel}.")
        except Exception as e:
            messagebox.showwarning("",F"¡No se pudo actualizar el nivel del personaje llamado {self.nombre}.! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def aumentar_experiencia(self,id_ingresado,experiencia_actualizada):
        try:
            cursor, connection = obtener_cursor()
            self.experiencia += experiencia_actualizada
            cursor.execute("""update personaje set experiencia = :1 where id = :2""", (self.experiencia,id_ingresado))    
            connection.commit()
            messagebox.showinfo("",F"Se ha actualizado la experiencia del personaje: {self.nombre} ha aumentado {experiencia_actualizada} de experiencia, ahora tiene {self.experiencia}.")
        except Exception as e:
            messagebox.showwarning("",F"¡No se pudo actualizar la experiencia del personaje llamado {self.nombre}.! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def mostrar_datos_personaje(self,id_ingresado):
        try:  
            messagebox.showinfo("Personaje_Encontrado",F"El personaje con id: {id_ingresado}, se llama: {self.nombre}, su nivel es: {self.nivel}, tiene {self.salud} de salud y su experiencia es de {self.experiencia}")
        except:
            messagebox.showwarning("Error",F"¡No se pudo encotrar los datos del personaje: {self.nombre}.!")

    def mostrar_armas_personaje(self,id_ingresado):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""SELECT a.id AS arma_id, a.tipo FROM personaje p JOIN arma_personaje ap ON p.id = ap.personaje_FK JOIN arma a ON ap.arma_FK = a.id WHERE p.id = :1""",(id_ingresado,))
            resultado = cursor.fetchall()
            if resultado:
                lista_armas = []
                for arma in resultado:
                    lista_armas.append(arma)
                messagebox.showinfo("Armas del Personaje",F"El personaje {self.nombre} tiene las armas: {lista_armas}")
            else:
                messagebox.showinfo("Armas del Personaje",F"{self.nombre} no tiene ninguna arma equipada.")
           
        except Exception as e:
            messagebox.showwarning("","¡No se pudo realizar la consulta correctamente.! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()
        
    def eliminar_personaje(self,id_ingresado):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""DELETE FROM personaje WHERE id = :1""", (id_ingresado,))   
            connection.commit()
            messagebox.showinfo("",F"Se ha eliminado al personaje con id: {id_ingresado} llamado: {self.nombre}")
        except ora.DatabaseError as e: 
            error, = e.args  
            if error.code == 2292:  
                messagebox.showwarning("", f"No se puede eliminar el Personaje {self.nombre} porque tiene armas en su inventario")
            else:
                messagebox.showwarning("", f"¡No se ha podido eliminar el Personaje: {self.tipo}! ERROR: {error.message}")
        except Exception as e:
            messagebox.showwarning("", f"¡No se ha podido eliminar el Personaje: {self.tipo}! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

def instanciar_personaje(nombre,nivel,salud,experiencia):
    objeto_personaje = Personaje(nombre,nivel,salud,experiencia)
    return objeto_personaje
    
def instanciar_personaje_de_bd(id_ingresado):
    if verificar_id_personaje(id_ingresado):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""SELECT nombre, nivel, salud, experiencia FROM personaje WHERE id = :1""", (id_ingresado,))
            resultado = cursor.fetchone()  # Esto nos devuelve una tupla con los valores: (nombre, nivel, salud, experiencia)
            nombre, nivel, salud, experiencia = resultado
            objeto_personaje = Personaje(nombre, nivel, salud, experiencia)
            return objeto_personaje
            
        except:
            messagebox.showwarning("",F"No se pudo extraer los datos del personaje con el id: {id_ingresado} para instanciarlo.")
        finally:
            cursor.close()
            connection.close()
    else:
        messagebox.showwarning("","Personaje_No_Encontrado",f"¡No existe el id {id_ingresado} ingresado o fue mal ingresado!")
        return None
       
    
def verificar_id_personaje(id_ingresado):
    try:
        cursor, connection = obtener_cursor()
        cursor.execute("SELECT id FROM personaje WHERE id = :1", (id_ingresado,))
        resultado = cursor.fetchone()
    

        if resultado and resultado[0] == id_ingresado:
            return True
        else:
            return False
    except Exception as e:
        messagebox.showwarning("Error",f"{e}")
    finally:
        cursor.close()
        connection.close()

def boton_mostrar_personaje(id_ingresado):
    objeto_personaje = instanciar_personaje_de_bd(id_ingresado)
    if objeto_personaje:
        objeto_personaje.mostrar_datos_personaje(id_ingresado)

def boton_crear_personaje(nombre,nivel,salud,experiencia):
    #intentar con la caja como variable y despues con el .get() para sacar variable
    objeto_personaje = instanciar_personaje(nombre,nivel,salud,experiencia)
    if objeto_personaje:
        objeto_personaje.crear_personaje()
        
def boton_actualizar_experiencia(id_ingresado,experiencia_actualizada):
    objeto_personaje = instanciar_personaje_de_bd(id_ingresado)
    if objeto_personaje:
        objeto_personaje.aumentar_experiencia(id_ingresado,experiencia_actualizada)  

def boton_actualizar_nivel(id_ingresado,nivel_actualizado):
    objeto_personaje = instanciar_personaje_de_bd(id_ingresado)
    if objeto_personaje:
        objeto_personaje.aumentar_nivel(id_ingresado,nivel_actualizado)
            
def boton_eliminar_personaje(id_ingresado):
    objeto_personaje = instanciar_personaje_de_bd(id_ingresado)
    if objeto_personaje:
        objeto_personaje.eliminar_personaje(id_ingresado)

def boton_mostrar_arma_personaje(id_ingresado):
    objeto_personaje = instanciar_personaje_de_bd(id_ingresado)
    if objeto_personaje:
        objeto_personaje.mostrar_armas_personaje(id_ingresado)
