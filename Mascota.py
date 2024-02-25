import datetime
from graphviz import Digraph  # Importar la clase Digraph desde la librería Graphviz

class Mascota:
    def __init__(self, id, nombre, energia=1, tipo="gato", estado="vivo"):
        self.id = id
        self.nombre = nombre
        self.energia = energia
        self.tipo = tipo
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Energía: {self.energia}, Tipo: {self.tipo}, Estado: {self.estado}"

class MascotaFinal:
    def __init__(self, nombre, energia_final, tipo, estado):
        self.nombre = nombre
        self.energia_final = energia_final
        self.tipo = tipo
        self.estado = estado

# Función para cargar mascotas desde un archivo
def cargar_mascotas_desde_archivo(nombre_archivo):
    gatos = []
    with open(nombre_archivo, 'r', encoding='cp1252') as file:
        lineas = file.readlines()

    for idx, linea in enumerate(lineas, start=1):
        partes = [parte.strip() for parte in linea.split(':')]
        if len(partes) > 1:
            comando, parametros = partes[0], partes[1]
            if comando == "Crear_Gato":
                parametros_divididos = parametros.split(',')
                nombre_gato = parametros_divididos[0]
                tipo_gato = parametros_divididos[1].strip() if len(parametros_divididos) > 1 else "gato"
                estado_gato = parametros_divididos[2].strip() if len(parametros_divididos) > 2 else "vivo"
                nuevo_gato = Mascota(idx, nombre_gato, tipo=tipo_gato, estado=estado_gato)
                gatos.append(nuevo_gato)
                imprimir_mensajes_acciones(nuevo_gato, "Crear_Gato", nuevo_gato.energia, nuevo_gato.energia, "mascotas.petworld_result")
            elif comando == "Dar_de_Comer":
                nombre_gato, peso_ratón = parametros.split(',')
                for gato in gatos:
                    if gato.nombre == nombre_gato:
                        energia_antes = gato.energia
                        gato.energia += 12 + int(peso_ratón)
                        imprimir_mensajes_acciones(gato, "Dar_de_Comer", energia_antes, gato.energia, "mascotas.petworld_result")
            elif comando == "Jugar":
                nombre_gato, tiempo = parametros.split(',')
                for gato in gatos:
                    if gato.nombre == nombre_gato:
                        energia_antes = gato.energia
                        gato.energia -= int(tiempo) // 2  # Corregido aquí
                        imprimir_mensajes_acciones(gato, "Jugar", energia_antes, gato.energia, "mascotas.petworld_result")
    return gatos

# Función para generar el gráfico PNG
def generar_grafico(mascotas_finales):
    dot = Digraph(comment='Mascotas')

    for mascota in mascotas_finales:
        dot.node(f'{mascota.nombre}', f'Nombre: {mascota.nombre}\nEnergía Final: {mascota.energia_final}\nTipo: {mascota.tipo}\nEstado: {mascota.estado}')

    dot.render('mascotas', format='png', cleanup=True)

# Función para imprimir mensajes de acciones
def imprimir_mensajes_acciones(gato, accion, energia_antes, energia_despues, output_file=None):
    now = datetime.datetime.now()

    if output_file:
        with open(output_file, 'a', encoding='utf-8') as file:
            if accion == "Crear_Gato":
                file.write("*" * 50 + "\n")
                file.write(f"[{now}] Se creó el gato {gato.nombre}\n")
            elif accion == "Dar_de_Comer":
                file.write(f"[{now}] le diste de comer a {gato.nombre}, su energia: Antes: {energia_antes}, Ahora: {energia_despues}\n")
            elif accion == "Jugar":
                file.write(f"[{now}] Jugaste con {gato.nombre}, su energia: Antes: {energia_antes}, Ahora: {energia_despues}\n")
                if energia_despues <= 0:
                    gato.estado = "muerto"
                    file.write(f"[{now}] El gato {gato.nombre} ha muerto debido a la falta de energía.\n")
                    file.write("[{}] Chales ya me morí\n".format(now))
                    file.write("\n--------------Resumen Global--------------------------\n")
                    file.write(f"{gato.nombre}, {gato.energia}, {gato.tipo}, {gato.estado}\n")
                    file.write("*" * 50 + "\n")
                else:
                    file.write("\n--------------Resumen Global--------------------------\n")
                    file.write(f"{gato.nombre}, {gato.energia}, {gato.tipo}, {gato.estado}\n")
                    file.write("*" * 50 + "\n")

    # Ahora también imprimimos en la consola
    if accion == "Crear_Gato":
        print("*" * 50)  # Separador antes de crear un nuevo gato
        print(f"[{now}] Se creó el gato {gato.nombre}")
    elif accion == "Dar_de_Comer":
        print(f"[{now}] le diste de comer a {gato.nombre}, su energia: Antes: {energia_antes}, Ahora: {energia_despues}")
    elif accion == "Jugar":
        print(f"[{now}] Jugaste con {gato.nombre}, su energia: Antes: {energia_antes}, Ahora: {energia_despues}")
        if energia_despues <= 0:
            gato.estado = "muerto"
            print(f"[{now}] El gato {gato.nombre} ha muerto debido a la falta de energía.")
            print("[{}] Chales ya me morí".format(now))
            print("\n--------------Resumen Global--------------------------")
            print(f"{gato.nombre}, {gato.energia}, {gato.tipo}, {gato.estado}")
            print("*" * 50)  # Separador solo después de jugar
        else:
            print("\n--------------Resumen Global--------------------------")
            print(f"{gato.nombre}, {gato.energia}, {gato.tipo}, {gato.estado}")
            print("*" * 50)  # Separador solo después de jugar

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
            gatos = cargar_mascotas_desde_archivo("mascotas.petmanager")
            # Crear la lista de mascotas finales para generar el gráfico
            mascotas_finales = []
            for gato in gatos:
                mascota_final = MascotaFinal(gato.nombre, gato.energia, gato.tipo, gato.estado)
                mascotas_finales.append(mascota_final)
            # Generar el gráfico PNG
            generar_grafico(mascotas_finales)
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, elige una opción válida.")

# Llamar al menú principal al iniciar el programa
menu_principal()
