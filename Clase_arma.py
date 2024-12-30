from Clase_personaje import*

#Creamos la clase arma.
class Arma():
    def __init__(self,tipo,dano,municiones):
            self.tipo = tipo
            self.dano = dano
            self.municiones = municiones
    
    #utilizamos metodo string en caso de que tenga que imprimirse.
    def __str__(self):
        return F"tipo: {self.tipo}, daño: {self.dano}, municiones: {self.municiones}"

    #Metodo que creara arma y realizara CRUD.
    def crear_arma(self):
        #Usamos try-except-finally al realizar el CRUD para asegurar controlar errores y cerrar la conexion siempre.
        try:
            #se usan las funciones del modulo conexion para crear la conexion y el cursor.
            cursor, connection = obtener_cursor()
            #En el execute se utilizara lenguaje SQL para interactuar con la base de datos, ademas se ocupa una secuencia para los ids de forma automatica.
            cursor.execute("""insert into arma values(seq_id_arma.nextval, :1, :2, :3)""", (self.tipo, self.dano, self.municiones))     
            connection.commit() 
            #Usamos messagebox en vez de print para que el usuario visualize lo que ocurre con su accion.
            messagebox.showinfo("",F"Se ha realizado la inserción del arma: {self.tipo} correctamente.")
        except Exception as e:
            messagebox.showwarning("",F"No se pudo realizar la inserción. ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def actualizar_arma(self,id_ingresado,tipo_actualizado,dano_actualizado,municiones_actualizada):
        try:
            cursor, connection = obtener_cursor()
            self.tipo = tipo_actualizado           
            self.dano = dano_actualizado
            self.municiones = municiones_actualizada
            cursor.execute("""update arma set tipo = :1 where id = :2""", (self.tipo, id_ingresado))
            cursor.execute("""update arma set dano = :1 where id = :2""", (self.dano, id_ingresado))
            cursor.execute("""update arma set municiones = :1 where id = :2""", (self.municiones, id_ingresado))     
            connection.commit()
            messagebox.showinfo("",F"Se ha actualizado el arma: {self.tipo}.")
        except Exception as e:
            messagebox.showwarning("",F"¡No se pudo actualizar el arma: {self.tipo}.! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def eliminar_arma(self,id_ingresado):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""delete from arma where id = :1""", (id_ingresado,))        
            connection.commit()
            messagebox.showinfo("",F"Se ha eliminado el arma {self.tipo}.")
        #Permite controlar el error que ocurre al intentar borrar una clave primaria utilizada por otra tabla.
        except ora.DatabaseError as e: 
            error, = e.args  
            if error.code == 2292:  
                messagebox.showwarning("", f"No se puede eliminar el arma {self.tipo} porque está equipada en un personaje.")
            else:
                messagebox.showwarning("", f"¡No se ha podido eliminar el arma: {self.tipo}! ERROR: {error.message}")
        except Exception as e:
            messagebox.showwarning("", f"¡No se ha podido eliminar el arma: {self.tipo}! ERROR: {e}")
        finally:
            cursor.close()
            connection.close()

    def mostrar_informacion_arma(self,id_ingresado):
        try:   
            messagebox.showinfo("",F"El arma con el id: {id_ingresado}, es de tipo: {self.tipo}, hace un daño de: {self.dano} y tiene como munición: {self.municiones}.")
        except:
            messagebox.showwarning("",F"¡No se pudo encontrar los datos del arma tipo: {self.tipo}!")

#Esta funcion instancia el objeto de la clase arma con datos entregados por el usuario.
def instanciar_arma(tipo,dano,municiones):
        objeto_arma = Arma(tipo,dano,municiones)
        return objeto_arma

#Esta funcion instancia el objeto de la clase arma con datos de la base de dato .
def instanciar_arma_de_bd(id_ingresado):
    if verificar_id_arma(id_ingresado):
        try:
            cursor, connection = obtener_cursor()
            cursor.execute("""SELECT tipo, dano, municiones FROM arma WHERE id = :1""", (id_ingresado,))
            resultado = cursor.fetchone()  
            tipo, dano, municiones = resultado
            objeto_arma = Arma(tipo, dano, municiones)
            return objeto_arma
        except:
                messagebox.showwarning("",F"No se pudo extraer los datos del arma con el id: {id_ingresado}")
        finally:
            cursor.close()
            connection.close()
    else:
        messagebox.showwarning("","¡No existe el ID ingresado o fue mal ingresado!")
        return None

#Esta funcion verifica la existencia del arma en la base de datos.
def verificar_id_arma(id_ingresado):
    try:
        cursor, connection = obtener_cursor()
        cursor.execute("SELECT id FROM arma WHERE id = :1", (id_ingresado,))
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

#Las siguientes funciones son las que utilizara la interfaz para realizar las operaciones CRUD, estas se componen de los metodos y las funciones de instanciar.
def boton_asignar_arma(id_personaje,municion_disponible,id_arma):
    objeto_personaje = instanciar_personaje_de_bd(id_personaje)
    objeto_arma = instanciar_arma_de_bd(id_arma)
    if objeto_personaje and objeto_arma:
        objeto_personaje.asignar_arma_personaje(id_personaje,municion_disponible,id_arma)

def boton_crear_arma(tipo,dano,municiones):
    objeto_arma = instanciar_arma(tipo,dano,municiones)
    if objeto_arma:
        objeto_arma.crear_arma()

def boton_actualizar_arma(id_ingresado,tipo_actualizado,dano_actualizado,municiones_actualizada):
    objeto_arma = instanciar_arma_de_bd(id_ingresado)
    if objeto_arma:
        objeto_arma.actualizar_arma(id_ingresado,tipo_actualizado,dano_actualizado,municiones_actualizada)

def boton_eliminar_arma(id_ingresado):
    objeto_arma = instanciar_arma_de_bd(id_ingresado)
    if objeto_arma:
        objeto_arma.eliminar_arma(id_ingresado)

def boton_mostrar_arma(id_ingresado):
    objeto_arma = instanciar_arma_de_bd(id_ingresado)
    if objeto_arma:
        objeto_arma.mostrar_informacion_arma(id_ingresado)

def boton_quitar_arma_personaje(id_personaje,id_arma):
    objeto_personaje = instanciar_personaje_de_bd(id_personaje)
    objeto_arma = instanciar_arma_de_bd(id_arma)
    if objeto_personaje and objeto_arma:
        objeto_personaje.quitar_arma_personaje(id_personaje,id_arma)