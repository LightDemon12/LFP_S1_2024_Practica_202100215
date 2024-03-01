import tkinter as tk
from tkinter import filedialog
import datetime
from graphviz import Digraph  
import os

# Clase para la mascota
class Mascota:
    def __init__(self, id, nombre, energia=1, tipo="gato", estado="vivo"):
        self.id = id
        self.nombre = nombre
        self.energia = energia
        self.tipo = tipo
        self.estado = estado
# Método para imprimir la información de la mascota
    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Energía: {self.energia}, Tipo: {self.tipo}, Estado: {self.estado}"
# Clase para el resumen final de las mascotas
class MascotaFinal:
    def __init__(self, nombre, energia_final, tipo, estado):
        self.nombre = nombre
        self.energia_final = energia_final
        self.tipo = tipo
        self.estado = estado
# Función para cargar mascotas desde un archivo
def cargar_mascotas_desde_archivo():
    root = tk.Tk()
    root.withdraw() # Ocultar la ventana principal 
    nombre_archivo = filedialog.askopenfilename(title="Selecciona el archivo de instrucciones", filetypes=[("PetManager files", "*.petmanager")])    
    gatos = []
    instrucciones = []
    with open(nombre_archivo, 'r', encoding='cp1252') as file:
        lineas = file.readlines()
    # Solicitar el nombre del archivo .petworld_result una vez utilizando tkinter
    nombre_archivo_result = filedialog.asksaveasfilename(defaultextension=".petworld_result", filetypes=[("PetWorld Result files", "*.petworld_result")], title="Guardar archivo .petworld_result")
    if nombre_archivo_result:
        nombre_archivo_result = os.path.splitext(nombre_archivo_result)[0] + ".petworld_result"
    else:
        # Si el usuario cancela la selección, utilizar un nombre predeterminado
        nombre_archivo_result = "mascotas.petworld_result"
    for idx, linea in enumerate(lineas, start=1):
        partes = [parte.strip() for parte in linea.split(':')]
        if len(partes) > 1:
            comando, parametros = partes[0], partes[1]
            instrucciones.append((comando, parametros))
    for idx, (comando, parametros) in enumerate(instrucciones, start=1):
        if comando == "Crear_Gato":
            parametros_divididos = parametros.split(',')
            nombre_gato = parametros_divididos[0]
            tipo_gato = parametros_divididos[1].strip() if len(parametros_divididos) > 1 else "gato"
            estado_gato = parametros_divididos[2].strip() if len(parametros_divididos) > 2 else "vivo"
            nuevo_gato = Mascota(idx, nombre_gato, tipo=tipo_gato, estado=estado_gato)
            gatos.append(nuevo_gato)
            imprimir_mensajes_acciones(nuevo_gato, "Crear_Gato", nuevo_gato.energia, nuevo_gato.energia, nombre_archivo_result)
        elif comando == "Dar_de_Comer":
            nombre_gato, peso_ratón = parametros.split(',')
            for gato in gatos:
                if gato.nombre == nombre_gato and gato.estado != "muerto":
                    energia_antes = gato.energia
                    gato.energia += 12 + int(peso_ratón)
                    imprimir_mensajes_acciones(gato, "Dar_de_Comer", energia_antes, gato.energia, nombre_archivo_result)
                    break  # Salir del bucle una vez que se encuentra la mascota
        elif comando == "Jugar":
            nombre_gato, tiempo = parametros.split(',')
            for gato in gatos:
                if gato.nombre == nombre_gato and gato.estado != "muerto":
                    energia_antes = gato.energia
                    gato.energia -= int(tiempo) // 2
                    imprimir_mensajes_acciones(gato, "Jugar", energia_antes, gato.energia, nombre_archivo_result)
                    if gato.energia <= 0:
                        gato.estado = "muerto"
                        imprimir_mensajes_acciones(gato, "Muerte", energia_antes, gato.energia, nombre_archivo_result)
                    break  # Salir del bucle una vez que se encuentra la mascota
        elif comando == "Resumen_Mascota":
            nombre_gato = parametros.strip()
            for gato in gatos:
                if gato.nombre == nombre_gato:
                    print(gato)
        elif comando == "Resumen_Global":
            for gato in gatos:
                print(gato)
    return [MascotaFinal(gato.nombre, gato.energia, gato.tipo, gato.estado) for gato in gatos]

# Función para generar el gráfico PNG
def generar_grafico(mascotas_finales):
    dot = Digraph(comment='Mascotas')
    for mascota in mascotas_finales:
        # Nodo central con el nombre del gato
        dot.node(f'{mascota.nombre}', f'Nombre: {mascota.nombre}')
        # Nodos para la energía, estado y tipo, apuntando al nodo central
        dot.node(f'{mascota.nombre}_energia', f'Energía: {mascota.energia_final}')
        dot.node(f'{mascota.nombre}_estado', f'Estado: {mascota.estado}')
        dot.node(f'{mascota.nombre}_tipo', f'Tipo: {mascota.tipo}')
        dot.edge(f'{mascota.nombre}', f'{mascota.nombre}_energia')
        dot.edge(f'{mascota.nombre}', f'{mascota.nombre}_estado')
        dot.edge(f'{mascota.nombre}', f'{mascota.nombre}_tipo')
    # Solicitar al usuario el nombre del archivo sin extensión
    nombre_archivo_png = filedialog.asksaveasfilename(defaultextension="", filetypes=[("PNG files", "*.png")], title="Guardar gráfico PNG")
    if nombre_archivo_png:
        # Corregir la extensión del archivo
        nombre_archivo_png = os.path.splitext(nombre_archivo_png)[0] + ".png"
        dot.render(nombre_archivo_png, format='png', cleanup=True)
# Función para imprimir mensajes de acciones
def imprimir_mensajes_acciones(gato, accion, energia_antes, energia_despues, output_file=None):
    now = datetime.datetime.now()
    if output_file is None:
        output_file = input("Ingrese el nombre del archivo .petworld_result: ")
        output_file = output_file.strip() + ".petworld_result"
    with open(output_file, 'a+', encoding='utf-8') as file:
        if accion == "Crear_Gato":
            file.write(f"[{now}] Se creó el gato {gato.nombre}\n")
        elif accion == "Dar_de_Comer":
            file.write(f"[{now}] Le diste de comer a {gato.nombre}, su energía antes: {energia_antes}, ahora: {energia_despues}\n")
        elif accion == "Jugar":
            file.write(f"[{now}] Jugaste con {gato.nombre}, su energía antes: {energia_antes}, ahora: {energia_despues}\n")
        elif accion == "Muerte":
            file.write(f"[{now}] El gato {gato.nombre} ha muerto debido a la falta de energía.\n")
            file.write("[{}] Chales ya me morí\n".format(now))
            file.write(f"{gato.nombre}, {energia_despues}, {gato.tipo}, {gato.estado}\n")
    if accion == "Crear_Gato":
        print(f"[{now}] Se creó el gato {gato.nombre}")
    elif accion == "Dar_de_Comer":
        print(f"[{now}] Le diste de comer a {gato.nombre}, su energía: antes: {energia_antes}, ahora: {energia_despues}")
    elif accion == "Jugar":
        print(f"[{now}] Jugaste con {gato.nombre}, su energía: antes: {energia_antes}, ahora: {energia_despues}")
    elif accion == "Muerte":
        print(f"[{now}] El gato {gato.nombre} ha muerto debido a la falta de energía.")
        print("[{}] Chales ya me morí".format(now))
        print(f"{gato.nombre}, {energia_despues}, {gato.tipo}, {gato.estado}")
# Función para el menú principal
def menu_principal():
    print("BIENVENIDO AL PET MANAGER")
    print("Presiona Enter para continuar...")
    input()
    menu_opciones()
# Función para el menú de opciones
def menu_opciones():
    while True:
        print("\n--- MENÚ ---")
        print("1. Módulo PetManager")
        print("2. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            mascotas_finales = cargar_mascotas_desde_archivo()
            if mascotas_finales:
                generar_grafico(mascotas_finales)
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, elige una opción válida.")
# Llamar al menú principal al iniciar el programa
menu_principal()
