from tkinter import ttk, messagebox
import tkinter as tk
from Clase_arma import *
from Clase_personaje import *
from Conexion import *

#Funcion que comprueba las armas que posee un personaje.
def comprobar_armas_asignadas(id_personaje):
    try:
        cursor, connection = obtener_cursor()
        cursor.execute("""SELECT COUNT(*) FROM arma_personaje WHERE personaje_FK = :1""",(id_personaje,))
        armas_asignadas = cursor.fetchone()

        if armas_asignadas:
            return armas_asignadas[0]
        else:
            return 0

    except Exception as e:
        print(F"hubo un error al contar las armas del personaje, ERROR: {e}")
    finally:
        cursor.close()
        connection.close()

#funcion que comprueba su la variable ingresada es entero y retorna un booleano.
def comprobar_entero(variable):
    try:
        int(variable)
        return True
    except ValueError:
        return False

#Inicio de la seccion para las opciones de personajes
def opciones_personaje():
    ventana_personaje = tk.Toplevel(ventana)
    ventana_personaje.title("Personaje")
    ventana_personaje.geometry("500x500")

    frame_opciones_personaje = ttk.Labelframe(ventana_personaje, text="Selecciona una opcion",padding=100,borderwidth=2,relief="groove")
    frame_opciones_personaje.grid(row=0, column=0, padx=60, pady=5)

    boton_opcion_1 = ttk.Button(frame_opciones_personaje, text="Crear", command=lambda: interfaz_crear_personaje(frame_opciones_personaje))
    boton_opcion_1.grid(row=1,column=0, pady=10)
    boton_opcion_2 = ttk.Button(frame_opciones_personaje, text="Borrar", command=lambda: interfaz_borrar_personaje(frame_opciones_personaje))
    boton_opcion_2.grid(row=2,column=0, pady=10)
    boton_opcion_3 = ttk.Button(frame_opciones_personaje, text="Actualizar_Nivel", command=lambda: interfaz_actualizar_nivel(frame_opciones_personaje))
    boton_opcion_3.grid(row=3,column=0, pady=10)
    boton_opcion_4 = ttk.Button(frame_opciones_personaje, text="Actualizar_XP", command=lambda: interfaz_actualizar_experiencia(frame_opciones_personaje))
    boton_opcion_4.grid(row=4,column=0, pady=10)
    boton_opcion_4 = ttk.Button(frame_opciones_personaje, text="Mostrar_Personaje", command=lambda: interfaz_mostrar_personaje(frame_opciones_personaje))
    boton_opcion_4.grid(row=5,column=0, pady=10)
    boton_cerrar = tk.Button(frame_opciones_personaje, text="Cerrar", command=ventana_personaje.destroy)
    boton_cerrar.grid(row=6,column=0, pady=10)


    def interfaz_crear_personaje(frame_opciones_personaje):
        for widget in frame_opciones_personaje.winfo_children():
            widget.grid_forget()

        #Casillas para llenar los datos de crear personaje
        ttk.Label(frame_opciones_personaje,text="Nombre", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_nombre = ttk.Entry(frame_opciones_personaje,width=10)
        caja_nombre.grid(row=1, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_personaje,text="Nivel", borderwidth=2).grid(row=2, column=0, padx=2, pady=3)
        caja_nivel = ttk.Entry(frame_opciones_personaje,width=10)
        caja_nivel.grid(row=3, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_personaje,text="Salud", borderwidth=2).grid(row=4, column=0, padx=2, pady=3)
        caja_salud = ttk.Entry(frame_opciones_personaje,width=10)
        caja_salud.grid(row=5, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_personaje,text="Exp", borderwidth=2).grid(row=6, column=0, padx=2, pady=3)
        caja_experiencia = ttk.Entry(frame_opciones_personaje,width=10)
        caja_experiencia.grid(row=7, column=0, padx=2, pady=3)

        # Botón que obtiene los valores de las entradas para crear personaje.
        def obtener_valores_crear_personaje():
            # Obtener los valores ingresados en las cajas de texto
            nombre = caja_nombre.get()
            nivel = caja_nivel.get()
            salud = caja_salud.get()
            experiencia = caja_experiencia.get()

            # Sanitizacion
            if not nombre or not nivel or not salud or not experiencia:
                messagebox.showwarning("Casillas vacias","¡Todos los campos deben ser completados!")
                ventana_personaje.destroy()
                return
            elif not len(nombre) <= 20:
                messagebox.showwarning("Nombre Demasiado Largo","El nombre debe ser menor o igual a 20 caracteres.")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(nivel):
                messagebox.showwarning("Nivel Invalido","El nivel debe ser un número entero.")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(salud):
                messagebox.showwarning("Salud Invalida","La salud debe ser un número entero.")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(experiencia):
                messagebox.showwarning("Experiencia invalida","La experiencia debe ser un número entero.")
                ventana_personaje.destroy()
                return

            nivel = int(nivel)
            salud = int(salud)
            experiencia = int(experiencia)

            # Llamar la función de crear personaje
            boton_crear_personaje(nombre, nivel, salud, experiencia)
            obtener_datos_personaje()
            ventana_personaje.destroy()
            

        # Botón para llamar la función que crea el personaje
        boton_crear_personaje_tk = tk.Button(frame_opciones_personaje, text="Crear", command=obtener_valores_crear_personaje)
        boton_crear_personaje_tk.grid(row=8, column=0, pady=30)
        


    def interfaz_borrar_personaje(frame_opciones_personaje):
        for widget in frame_opciones_personaje.winfo_children():
            widget.grid_forget()

        #Casilla para ingresar la id del personaje
        ttk.Label(frame_opciones_personaje,text="ID_Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=10)
        caja_para_borrar = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_borrar.grid(row=1, column=0, padx=2, pady=10)

        def obtener_valores_eliminar_personaje():
            #Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_para_borrar.get()

            #Sanitizacion
            if not id_ingresado:
                messagebox.showwarning("Casilla Incompleta","¡Todos los campos deben ser completados!")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_personaje.destroy()
                return

            id_ingresado = int(id_ingresado)

            #Llamar la función de crear personaje
            boton_eliminar_personaje(id_ingresado)
            obtener_datos_personaje()
            ventana_personaje.destroy()

        #Boton para borrar al personaje de la id ingresada
        boton_borrar_personaje = tk.Button(frame_opciones_personaje, text="Borrar", command=obtener_valores_eliminar_personaje)
        boton_borrar_personaje.grid(row=4,column=0, pady=30)


    def interfaz_actualizar_nivel(frame_opciones_personaje):
        for widget in frame_opciones_personaje.winfo_children():
            widget.grid_forget()

        #Casilla para buscar al personaje por la id
        ttk.Label(frame_opciones_personaje,text="ID_Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=10,)
        caja_para_id = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_id.grid(row=1, column=0, padx=2, pady=10)

        ttk.Label(frame_opciones_personaje,text="Aumentar_Nivel", borderwidth=2).grid(row=2, column=0, padx=2, pady=10,)
        caja_para_nivel = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_nivel.grid(row=3, column=0, padx=2, pady=10)

        def obtener_valores_actualizar_nivel():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_para_id.get()
            nivel_actualizado = caja_para_nivel.get()

            #Sanitizacion
            if not id_ingresado or not nivel_actualizado:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(nivel_actualizado):
                messagebox.showwarning("Error de valor","El nivel ha aumentar debe ser un número entero.")
                ventana_personaje.destroy()
                return

            id_ingresado = int(id_ingresado)
            nivel_actualizado =int(nivel_actualizado)

            # Llamar la función de crear personaje
            boton_actualizar_nivel(id_ingresado,nivel_actualizado)
            obtener_datos_personaje()
            ventana_personaje.destroy()


        boton_aumentar_nivel = tk.Button(frame_opciones_personaje, text="Incrementar_Nivel", command=obtener_valores_actualizar_nivel)
        boton_aumentar_nivel.grid(row=4,column=0, pady=30)


    def interfaz_actualizar_experiencia(frame_opciones_personaje):
        #Ocultar los botones anteriores
        for widget in frame_opciones_personaje.winfo_children():
            widget.grid_forget()
        
        #Casilla para buscar al personaje por la id
        ttk.Label(frame_opciones_personaje,text="ID_Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=10,)
        caja_para_id = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_id.grid(row=1, column=0, padx=2, pady=10)

        ttk.Label(frame_opciones_personaje,text="Aumento_Xp", borderwidth=2).grid(row=2, column=0, padx=2, pady=10,)
        caja_para_xp = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_xp.grid(row=3, column=0, padx=2, pady=10)

        def obtener_valores_actualizar_experiencia():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_para_id.get()
            experiencia_actualizada = caja_para_xp.get()

            # Sanitizacion
            if not id_ingresado or not experiencia_actualizada:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(experiencia_actualizada):
                messagebox.showwarning("Error de valor","la experiencia ha aumentar debe ser un número entero.")
                ventana_personaje.destroy()
                return

            id_ingresado = int(id_ingresado)
            experiencia_actualizada =int(experiencia_actualizada)

            # Llamar la función de crear personaje
            boton_actualizar_experiencia(id_ingresado,experiencia_actualizada)
            obtener_datos_personaje()
            ventana_personaje.destroy()

        boton_aumentar_experiencia = tk.Button(frame_opciones_personaje, text="Incrementar_Xp", command=obtener_valores_actualizar_experiencia)
        boton_aumentar_experiencia.grid(row=4,column=0, pady=30)


    def interfaz_mostrar_personaje(frame_opciones_personaje):
        for widget in frame_opciones_personaje.winfo_children():
            widget.grid_forget()
        
        ttk.Label(frame_opciones_personaje,text="ID_Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=10,)
        caja_para_id = ttk.Entry(frame_opciones_personaje,width=10)
        caja_para_id.grid(row=1, column=0, padx=2, pady=10)

        def obtener_valores_mostrar_personaje():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_para_id.get()

            # Sanitizacion
            if not id_ingresado:
                messagebox.showwarning("Casilla Incompleta","¡Todos los campos deben ser completados!")
                ventana_personaje.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_personaje.destroy()
                return

            id_ingresado = int(id_ingresado)

            # Llamar la función de crear personaje
            boton_mostrar_personaje(id_ingresado)
            ventana_personaje.destroy()

        boton_buscar_personaje = tk.Button(frame_opciones_personaje, text="Buscar_Personaje", command=obtener_valores_mostrar_personaje)
        boton_buscar_personaje.grid(row=2,column=0, pady=30)
    

#Termino de seccion Opciones de personaje/////////////////////////////////////////////////////////////////////////////////////////////


#Inicio de seccion para las opciones de las armas
def opciones_armas():
    ventana_armas = tk.Toplevel(ventana)
    ventana_armas.title("Armas")
    ventana_armas.geometry("500x500")

    frame_opciones_armas = ttk.Labelframe(ventana_armas, text="Selecciona una opcion",padding=100,borderwidth=2,relief="groove")
    frame_opciones_armas.grid(row=0, column=0, padx=60, pady=40)

    boton_opcion_1 = ttk.Button(frame_opciones_armas, text="Crear", command=lambda: interfaz_crear_arma(frame_opciones_armas))
    boton_opcion_1.grid(row=1,column=0, pady=10)
    boton_opcion_1 = ttk.Button(frame_opciones_armas, text="Datos_Arma", command=lambda: interfaz_mostrar_arma(frame_opciones_armas))
    boton_opcion_1.grid(row=2,column=0, pady=10)
    boton_opcion_2 = ttk.Button(frame_opciones_armas, text="Borrar", command=lambda: interfaz_borrar_Arma(frame_opciones_armas))
    boton_opcion_2.grid(row=3,column=0, pady=10)
    boton_opcion_3 = ttk.Button(frame_opciones_armas, text="Actualizar", command=lambda: interfaz_actualizar_arma(frame_opciones_armas))
    boton_opcion_3.grid(row=4,column=0, pady=10)
    boton_cerrar = tk.Button(frame_opciones_armas, text="Cerrar", command=ventana_armas.destroy)
    boton_cerrar.grid(row=5,column=0, pady=30)


    def interfaz_crear_arma(frame_opciones_armas):
        for widget in frame_opciones_armas.winfo_children():
            widget.grid_forget()

        #Casillas para ingresar los valores del arma
        ttk.Label(frame_opciones_armas,text="Tipo De Arma", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_tipo = ttk.Entry(frame_opciones_armas,width=10)
        caja_tipo.grid(row=1, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_armas,text="Daño Del Arma", borderwidth=2).grid(row=2, column=0, padx=2, pady=3)
        caja_dano = ttk.Entry(frame_opciones_armas,width=10)
        caja_dano.grid(row=3, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_armas,text="Municion o Usos", borderwidth=2).grid(row=4, column=0, padx=2, pady=3)
        caja_municion = ttk.Entry(frame_opciones_armas,width=10)
        caja_municion.grid(row=5, column=0, padx=2, pady=3)

        def obtener_valores_crear_arma():
            # Obtener los valores ingresados en las cajas de texto
            tipo = caja_tipo.get()
            dano = caja_dano.get()
            municiones = caja_municion.get()

            # Sanitizacion
            if not tipo or not dano or not municiones:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_armas.destroy()
                return
            elif not len(tipo) <= 20:
                messagebox.showwarning("Nombre muy Largo","El tipo debe ser menor o igual a 20 caracteres.")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(dano):
                messagebox.showwarning("Error de valor","El daño debe ser un número entero.")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(municiones):
                messagebox.showwarning("Error de valor","La municion debe ser un número entero.")
                ventana_armas.destroy()
                return

            dano = int(dano)
            municiones = int(municiones)

            # Llamar la función de crear arma
            boton_crear_arma(tipo,dano,municiones)
            obtener_datos_armas()
            ventana_armas.destroy()

        #Boton para crear las armas
        boton_crear_arma_tk = tk.Button(frame_opciones_armas, text="Crear", command=obtener_valores_crear_arma)
        boton_crear_arma_tk.grid(row=6,column=0, pady=30)


    def interfaz_borrar_Arma(frame_opciones_armas):
        for widget in frame_opciones_armas.winfo_children():
            widget.grid_forget()
        
        #Casilla para colocar la id del arma que se quiere eliminar
        ttk.Label(frame_opciones_armas,text="Id Del Arma", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id = ttk.Entry(frame_opciones_armas,width=10)
        caja_id.grid(row=1, column=0, padx=2, pady=3)

        def obtener_valores_eliminar_arma():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_id.get()

            # Sanitizacion
            if not id_ingresado:
                messagebox.showwarning("Casilla Incompleta","¡Todos los campos deben ser completados!")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_armas.destroy()
                return

            id_ingresado = int(id_ingresado)

            # Llamar la función de crear personaje
            boton_eliminar_arma(id_ingresado)
            obtener_datos_armas()
            ventana_armas.destroy()

        #boton para eliminar el arma 
        boton_borrar_arma_tk = tk.Button(frame_opciones_armas, text="Borrar", command=obtener_valores_eliminar_arma)
        boton_borrar_arma_tk.grid(row=8,column=0, pady=30)


    def interfaz_actualizar_arma(frame_opciones_armas):
        for widget in frame_opciones_armas.winfo_children():
            widget.grid_forget()

        ttk.Label(frame_opciones_armas,text="Id Del Arma", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id_arma = ttk.Entry(frame_opciones_armas,width=10)
        caja_id_arma.grid(row=1, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_armas,text="Ingresa los nuevos valores del arma", borderwidth=2).grid(row=2, column=0, padx=2, pady=10)

        #casillas para ingresar los nuevos datos del arma
        ttk.Label(frame_opciones_armas,text="Tipo De Arma", borderwidth=2).grid(row=3, column=0, padx=2, pady=3)
        caja_tipo = ttk.Entry(frame_opciones_armas,width=10)
        caja_tipo.grid(row=4, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_armas,text="Daño Del Arma", borderwidth=2).grid(row=5, column=0, padx=2, pady=3)
        caja_dano = ttk.Entry(frame_opciones_armas,width=10)
        caja_dano.grid(row=6, column=0, padx=2, pady=3)

        ttk.Label(frame_opciones_armas,text="Municion o Usos", borderwidth=2).grid(row=7, column=0, padx=2, pady=3)
        caja_municion = ttk.Entry(frame_opciones_armas,width=10)
        caja_municion.grid(row=8, column=0, padx=2, pady=3)

        def obtener_valores_actualizar_arma():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_id_arma.get()
            tipo_actualizado = caja_tipo.get()
            dano_actualizado = caja_dano.get()
            municion_actualizada = caja_municion.get()

            # Sanitizacion
            if not id_ingresado or not tipo_actualizado or not dano_actualizado or not municion_actualizada:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_armas.destroy()
                return
            elif not len(tipo_actualizado) <= 20:
                messagebox.showwarning("Error de valor","El tipo actualizado debe ser menor o igual a 20 caracteres.")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(dano_actualizado):
                messagebox.showwarning("Error de valor","El daño actualizado debe ser un número entero.")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(municion_actualizada):
                messagebox.showwarning("Error de valor","La municion actualizada debe ser un número entero.")
                ventana_armas.destroy()
                return

            id_ingresado = int(id_ingresado)
            dano_actualizado = int(dano_actualizado)
            municion_actualizada = int(municion_actualizada)

            # Llamar la función de crear personaje
            boton_actualizar_arma(id_ingresado,tipo_actualizado,dano_actualizado,municion_actualizada)
            obtener_datos_armas()
            ventana_armas.destroy()

        #Boton para actualizar a los nuevos datos ingresados
        boton_actualizar_arma_tk = tk.Button(frame_opciones_armas, text="Cambiar", command=obtener_valores_actualizar_arma)
        boton_actualizar_arma_tk.grid(row=9,column=0, pady=30)


    def interfaz_mostrar_arma(frame_opciones_armas):    
        for widget in frame_opciones_armas.winfo_children():
            widget.grid_forget()
        
        ttk.Label(frame_opciones_armas,text="ID_Arma", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id_arma = ttk.Entry(frame_opciones_armas,width=10)
        caja_id_arma.grid(row=1, column=0, padx=2, pady=3)

        def obtener_valores_mostrar_arma():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_id_arma.get()

            # Sanitizacion
            if not id_ingresado:
                messagebox.showwarning("Casilla Incompleta","¡Todos los campos deben ser completados!")
                ventana_armas.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_armas.destroy()
                return

            id_ingresado = int(id_ingresado)

            # Llamar la función de crear personaje
            boton_mostrar_arma(id_ingresado)
            ventana_armas.destroy()

        boton_mostrar_arma_tk = tk.Button(frame_opciones_armas, text="Mostrar_Datos", command=obtener_valores_mostrar_arma)
        boton_mostrar_arma_tk.grid(row=7,column=0, pady=30)


#Fin de opciones de armas//////////////////////////////////////////////////////////////////////////////////////////////////////


def opciones_equipamiento():
    ventana_equipamiento = tk.Toplevel(ventana)
    ventana_equipamiento.title("Equipo")
    ventana_equipamiento.geometry("500x500")

    frame_opciones_equipamiento = ttk.Labelframe(ventana_equipamiento, text="Selecciona una opcion",padding=100,borderwidth=2,relief="groove")
    frame_opciones_equipamiento.grid(row=0, column=0, padx=60, pady=40)

    boton_opcion_1 = ttk.Button(frame_opciones_equipamiento , text="Asignar", command=lambda: interfaz_asignar_arma(frame_opciones_equipamiento))
    boton_opcion_1.grid(row=1,column=0, pady=10)
    boton_opcion_2 = ttk.Button(frame_opciones_equipamiento , text="Quitar", command=lambda: interfaz_quitar_arma_asignada(frame_opciones_equipamiento))
    boton_opcion_2.grid(row=2,column=0, pady=10)
    boton_opcion_3 = ttk.Button(frame_opciones_equipamiento , text="Mostrar", command=lambda: interfaz_mostrar_equipamiento(frame_opciones_equipamiento))
    boton_opcion_3.grid(row=3,column=0, pady=10)
    boton_cerrar = tk.Button(frame_opciones_equipamiento , text="Cerrar", command=ventana_equipamiento.destroy)
    boton_cerrar.grid(row=4,column=0, pady=30)


    def interfaz_asignar_arma(frame_opciones_equipamiento):
        for widget in frame_opciones_equipamiento.winfo_children():
            widget.grid_forget()

        #casilla para la id del personaje que se quiere asignar el arma
        ttk.Label(frame_opciones_equipamiento,text="Id Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id_personaje = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_id_personaje.grid(row=1, column=0, padx=2, pady=3)

        #Casilla para la id del arma a la que se le asignara al personaje
        ttk.Label(frame_opciones_equipamiento,text="Id Arma", borderwidth=2).grid(row=2, column=0, padx=2, pady=3)
        caja_id_arma = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_id_arma.grid(row=3, column=0, padx=2, pady=3)

        #Casilla para la muncion disponible del arma a la que se le asignara al personaje
        ttk.Label(frame_opciones_equipamiento,text="Municion disponible", borderwidth=2).grid(row=4, column=0, padx=2, pady=3)
        caja_municion_disponible = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_municion_disponible.grid(row=5, column=0, padx=2, pady=3)

        def obtener_valores_asignar_arma():
            # Obtener los valores ingresados en las cajas de texto
            id_personaje = caja_id_personaje.get()
            municion_disponible = caja_municion_disponible.get()
            id_arma = caja_id_arma.get()

            # Sanitizacion
            if not id_personaje or not municion_disponible or not id_arma:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(id_personaje):
                messagebox.showwarning("Error de valor","El id del personaje debe ser un número entero.")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(municion_disponible):
                messagebox.showwarning("Error de valor","La municion disponible debe ser un número entero.")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(id_arma):
                messagebox.showwarning("Error de valor","El id del arma debe ser un número entero.")
                ventana_equipamiento.destroy()
                return

            id_personaje = int(id_personaje)
            municion_disponible = int(municion_disponible)
            id_arma = int(id_arma)
            
            armas_asignadas = comprobar_armas_asignadas(id_personaje)

            if armas_asignadas >= 3:
                messagebox.showwarning("Muchas Armas",f"El personaje {id_personaje} ya tiene 3 armas asignadas. No se pueden asignar más.")
                ventana_equipamiento.destroy()
                return
                

            # Llamar la función de crear personaje
            boton_asignar_arma(id_personaje,municion_disponible,id_arma)
            obtener_datos_equipo()
            ventana_equipamiento.destroy()

        #Boton para asignar el arma al personaje}
        boton_asignar_arma_tk = tk.Button(frame_opciones_equipamiento, text="Asinar_Arma", command=obtener_valores_asignar_arma)
        boton_asignar_arma_tk.grid(row=6,column=0, pady=30)


    def interfaz_quitar_arma_asignada(frame_opciones_equipamiento):
        for widget in frame_opciones_equipamiento.winfo_children():
            widget.grid_forget()

        #casilla para la id del personaje que se quiere quitar un arma
        ttk.Label(frame_opciones_equipamiento,text="Id Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id_personaje = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_id_personaje.grid(row=1, column=0, padx=2, pady=3)

        #Casilla para la id del arma a la que se le quitara al personaje
        ttk.Label(frame_opciones_equipamiento,text="Id Arma", borderwidth=2).grid(row=2, column=0, padx=2, pady=3)
        caja_id_arma = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_id_arma.grid(row=3, column=0, padx=2, pady=3)

        def obtener_valores_quitar_arma():
            # Obtener los valores ingresados en las cajas de texto
            id_personaje = caja_id_personaje.get()
            id_arma = caja_id_arma.get()

            # Sanitizacion
            if not id_personaje or not id_arma:
                messagebox.showwarning("Casillas Incompletas","¡Todos los campos deben ser completados!")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(id_personaje):
                messagebox.showwarning("Error de valor","El id del personaje debe ser un número entero.")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(id_arma):
                messagebox.showwarning("Error de valor","El id del arma debe ser un número entero.")
                ventana_equipamiento.destroy()
                return

            id_personaje = int(id_personaje)
            id_arma = int(id_arma)

            # Llamar la función de crear personaje
            boton_quitar_arma_personaje(id_personaje,id_arma)
            obtener_datos_equipo()
            ventana_equipamiento.destroy()

        #Boton para quitar el arma al personaje
        boton_quitar_arma_tk = tk.Button(frame_opciones_equipamiento, text="Quitar arma", command=obtener_valores_quitar_arma)
        boton_quitar_arma_tk.grid(row=4,column=0, pady=30)


    def interfaz_mostrar_equipamiento(frame_opciones_equipamiento):
        for widget in frame_opciones_equipamiento.winfo_children():
            widget.grid_forget()

        ttk.Label(frame_opciones_equipamiento,text="Id Personaje", borderwidth=2).grid(row=0, column=0, padx=2, pady=3)
        caja_id_personaje = ttk.Entry(frame_opciones_equipamiento,width=10)
        caja_id_personaje.grid(row=1, column=0, padx=2, pady=3)

        def obtener_valores_mostrar_equipamiento():
            # Obtener los valores ingresados en las cajas de texto
            id_ingresado = caja_id_personaje.get()

            # Sanitizacion
            if not id_ingresado:
                messagebox.showwarning("Casilla Incompleta","¡Todos los campos deben ser completados!")
                ventana_equipamiento.destroy()
                return
            elif not comprobar_entero(id_ingresado):
                messagebox.showwarning("Error de valor","El id ingresado debe ser un número entero.")
                ventana_equipamiento.destroy()
                return

            id_ingresado = int(id_ingresado)

            # Llamar la función de crear personaje
            boton_mostrar_arma_personaje(id_ingresado)
            ventana_equipamiento.destroy()

        boton_mostrar_equipo = tk.Button(frame_opciones_equipamiento, text="Mostrar", command=obtener_valores_mostrar_equipamiento)
        boton_mostrar_equipo.grid(row=4,column=0, pady=30)


#Final seccion de equipamiento////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#Inicio Ventana Principal////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#Ventana y configuracion de el porte de la misma
ventana = tk.Tk()
ventana.title("SISTEMA DE CRUD")
#Esta configuracion toma los portes de la pantalla donde se ejecuta el codigo para que ocupe toda la pantalla de inmediato
ventana.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}")
#Frame de menu que muestra los opciones principales
menu = ttk.Labelframe(ventana,text="MENU",padding=100,borderwidth=2,relief="groove")
menu.grid(row=0, column=1, padx=0, pady=0,sticky='n')
#Esta confuracion es para centralizar el frame de menu en la ventana


#Inicio del frame para mostrar los datos de la tabla Personaje//////////////////////////////////////////////////////////////////////////////////////
label_tabla_personajes = ttk.Labelframe(ventana, text="Tabla_Personajes", padding=100, borderwidth=2, relief="groove")
label_tabla_personajes.grid(row=1, column=0, padx=1, pady=1)

#Crear el tabla para ver datos de Personajes
tabla_personajes = ttk.Treeview(label_tabla_personajes, columns=("id", "nombre", "nivel", "salud", "experiencia"), show="headings")
tabla_personajes.pack()

#Nombrar las columnas para la tabla personaje
tabla_personajes.heading("id", text="ID")
tabla_personajes.heading("nombre", text="Nombre_Personaje")
tabla_personajes.heading("nivel", text="Nivel")
tabla_personajes.heading("salud", text="Salud")
tabla_personajes.heading("experiencia", text="Xp")

#Darle el tamaño a columnas 
tabla_personajes.column("id", width=30,anchor= "center")
tabla_personajes.column("nombre", width=100,anchor= "center")
tabla_personajes.column("nivel", width=50,anchor= "center")
tabla_personajes.column("salud", width=50,anchor= "center")
tabla_personajes.column("experiencia", width=80,anchor= "center")

#funcion para obejener los datos de la base de datos y mostrarlos en la tabla
def obtener_datos_personaje():
    try:
        connection = obtener_conexion() 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM personaje")
        datos = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in tabla_personajes.get_children():
            tabla_personajes.delete(row)

#Inserta los datos en la tabla
        for fila in datos:
            tabla_personajes.insert("", tk.END, values=fila)
        
    except Exception as e:
        print(f"Error al obtener los datos: {e}")

ventana.after(100, obtener_datos_personaje)


#Inicio de frame para mostrar los datos de la tabla Equipamiento (Tabla intermedia)///////////////////////////////////////////////////////////////////////////////////
label_tabla_equipamiento = ttk.Labelframe(ventana, text="Tabla_Equipamiento", padding=100, borderwidth=2, relief="groove")
label_tabla_equipamiento.grid(row=1, column=1, padx=20, pady=10)

#Crear la tabla para mostrar los datos 
tabla_equipamiento = ttk.Treeview(label_tabla_equipamiento, columns=("personaje", "armas", "municion"), show="headings")
tabla_equipamiento.pack()

#Nombrar las columnas de la tabla
tabla_equipamiento.heading("personaje", text="Personaje")
tabla_equipamiento.heading("armas", text="Armas")
tabla_equipamiento.heading("municion", text="Municion")

#darle el porte a las columnas
tabla_equipamiento.column("personaje", width=80,anchor= "center")
tabla_equipamiento.column("armas", width=120,anchor= "center")
tabla_equipamiento.column("municion", width=80,anchor= "center")

def obtener_datos_equipo():
    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("SELECT p.nombre, a.tipo, ap.municiones_disponibles FROM personaje p JOIN arma_personaje ap ON p.id = ap.personaje_FK JOIN arma a ON ap.arma_FK = a.id")
        datos = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in tabla_equipamiento.get_children():
            tabla_equipamiento.delete(row)

        #Inserta los datos en la tabla
        for fila in datos:
            tabla_equipamiento.insert("", tk.END, values=fila)
        
    except Exception as e:
        print(f"Error al obtener los datos: {e}")

ventana.after(100, obtener_datos_equipo)


#Inicio de frame para mostrar los datos de la tabla Armas////////////////////////////////////////////////////////////////////////////////////////
label_tabla_armas = ttk.Labelframe(ventana, text="Tabla_Armas", padding=100, borderwidth=2, relief="groove")
label_tabla_armas.grid(row=1, column=2, padx=20, pady=10, sticky='e')

#Crear tabla para mostrar los datos de la tabla arma
tabla_armas = ttk.Treeview(label_tabla_armas, columns=("id", "tipo", "danio", "municion"), show="headings")
tabla_armas.pack()

#Nombrar las columnas de la tabla
tabla_armas.heading("id", text="ID")
tabla_armas.heading("tipo", text="Tipo_arma")
tabla_armas.heading("danio", text="Daño")
tabla_armas.heading("municion", text="Municion")

#darle el porte a las columnas
tabla_armas.column("id", width=30,anchor= "center")
tabla_armas.column("tipo", width=120,anchor= "center")
tabla_armas.column("danio", width=50,anchor= "center")
tabla_armas.column("municion", width=80,anchor= "center")

#funnción para obtener datos de la tabla arma y insertarlos en la tabla 
def obtener_datos_armas():
    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM arma")
        datos = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in tabla_armas.get_children():
            tabla_armas.delete(row)

        #Inserta los datos en la tabla
        for fila in datos:
            tabla_armas.insert("", tk.END, values=fila)
        
    except Exception as e:
        print(f"Error al obtener los datos: {e}")

ventana.after(100, obtener_datos_armas)

#añadir un frame vacío al final de la ventana para asegurarse de que las tablas estén en la parte inferior respuesta de chatgpt funciono haci que lo dejamos no entendemos al 100% como funciona
ventana.grid_rowconfigure(2, weight=1)


#Boton para ingresar a la seccion de opciones de personaje
boton_personaje = ttk.Button(menu, text="Opciones de personaje", command=opciones_personaje)
boton_personaje.grid(row=0, column=0, pady=10)

#Boton para ingresar a la seccion de opciones de armas
boton_arma = ttk.Button(menu,text="Opciones de arma", command=opciones_armas)
boton_arma.grid(row=1, column=0, pady=10)

#Boron para ingresar a la seccion de opciones de equipamiento
boton_asignar = ttk.Button(menu,text="Opciones de equipamiento", command=opciones_equipamiento)
boton_asignar.grid(row=2, column=0, pady=10)

tk.mainloop()