#=================================#
#      GESTOR DE VACACIONES       #
#=================================#


## Bloque de constantes y datos ##
import csv
import unicodedata
import os
from datetime import datetime, timedelta
import hashlib
import time
from calendar import monthrange

##Datos de gerente
id_gerente = 123623
contraseña_gerente = "55b4b9575ace5c6f4b6ac19424120ffb38c5de51b59f88e4d61b49e2234782b9"

# menu opciones
menu_confirmacion = [0,1]
menu_c_dias =[0,1,2,3]
menu_sugerencias = [0,1,2]
menu_s_dias = [0,2,3]
menu_gerencia = [0,1,2,3,4,5]
menu_admin = [0,1,2,3,4,5,6,7]

# menu para mostrar
mostrar_menu_confirmacion = ["Confirmar. 0-No 1-Si"]
mostrar_menu_s_dias = ["2. Consultar historial y saldo",
                       "3. Modificar-cancelar",
                       "0. Salir"
                       ]
mostrar_menu_c_dias = ["1. Solicitar vacaciones",
                       "2. Consultar historial y saldo",
                       "3. Modificar-cancelar",
                       "0. Salir" ]
mostrar_menu_gerente = ["\n-----Menu Gerente-----\n",
                        "1. Consultar empleado",
                        "2. Estadísticas generales",
                        "3. Ver calendario de vacaciones",
                        "4. Ver registro del sistema",
                        "5. Acceder a administración",
                        "0. Cerrar sesión"]
mostrar_menu_admin = ["\n-----Menu Administrador-----\n",
                      "1. Desbloquear usuario",
                      "2. Reiniciar contraseña",
                      "3. Listar empleados",
                      "4. Consultar empleado",
                      "5. Listar vacaciones aprobadas",
                      "6. Cancelar vacaciones",
                      '7. Cerrar "Gestor de vacaciones"',
                      "0. Cerrar sesión"]


#registro txt
registro = []

#Rutas de datos
RUTA_EMPLEADOS = "empleados.csv"
RUTA_VACACIONES = "vacaciones_2026.csv"
RUTA_CALENDARIO = "calendario.csv"
RUTA_REGISTRO = "interacciones.txt"

#Columnas de csvs
COLUMNAS_CSVC =[[
    "legajo",
    "nombre",
    "clase",
    "antiguedad",
    "dias_disponibles",
    "contraseña",
    "acceso"],[
    "legajo",
    "fecha_solicitud",
    "fecha_inicio",
    "fecha_fin",
    "dias",
    "dias_restantes",
    "estado"],[
    "fecha",
    "clase1",
    "clase2",
    "clase3"]]




##_____Funciones_____##
def normalizar(texto):
    texto = texto.strip().lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn') 

##~~~Validaciones~~~##
def validar_numero(mensaje,entero=True):
 while True:
   try:
       entrada= input(mensaje).strip()
       ingreso = float(entrada) 
       if entero:
           return int(ingreso)
       return ingreso
   except ValueError:
          print (f"\nERROR: '{entrada}' no es un nunero valido.\n")
                  
def validar_menu(lis_mensajes,lista,numerico=True):
    while True:
        for linea in lis_mensajes:
            print(linea)
        print()    
        try:
            opcion = input("\nElija su opción: ").strip().capitalize()
            if numerico :
                opcion = int(opcion)
            if opcion in lista:
                return opcion
            print(f"\nOpción no válida. Opciones: {lista}\n")
            
        except ValueError:
            print("\nEntrada inválida. Ingrese un número\n")


##~~~Cifrado~~~##
def cifrar(texto):
    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()





##~~~Persistencia~~~##
def cargar_csv(ruta):

    try:

        with open(ruta,"r",encoding="utf-8") as archivo:

            return list(csv.DictReader(archivo))

    except FileNotFoundError:

        registrar(f"Archivo no encontrado: {ruta}")

        print(f"\nERROR: No se encontró {ruta}")

        return []

    except Exception as e:

        registrar(f"Error al cargar {ruta}: {e}")

        print(f"\nERROR al leer {ruta}")

        return []

def guardar_csv(lista,ruta_csv):

    if not lista:
        return
    
    columnas = list(lista[0].keys())   

    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
            destino = csv.DictWriter(archivo, fieldnames=columnas)
            destino.writeheader()
            destino.writerows(lista)

def carga_inicial():

    # empleados.csv es obligatorio
    if not os.path.exists(RUTA_EMPLEADOS):

        print(
            "\nERROR CRÍTICO"
            "\nNo existe empleados.csv"
            "\nGestor de Vacaciones fuera de servicio."
        )

        return None, None, None


    # interacciones.txt
    if not os.path.exists(RUTA_REGISTRO):

        with open(RUTA_REGISTRO,"w",encoding="utf-8"):
            registrar(f"Se creó {RUTA_REGISTRO}")


    # vacaciones_2026.csv
    if not os.path.exists(RUTA_VACACIONES):

            
        lista = [{
        "legajo": "Inicio",
        "fecha_solicitud": "Inicio",
        "fecha_inicio": "Inicio",
        "fecha_fin": "Inicio",
        "dias": "Inicio",
        "dias_restantes": "Inicio",
        "estado": "Inicio"}]

        columnas = list(lista[0].keys())

        with open(RUTA_VACACIONES, "w", newline="", encoding="utf-8") as archivo:
            destino = csv.DictWriter(archivo, fieldnames=columnas)
            destino.writeheader()
            destino.writerows(lista)
        registrar(f"Se creó {RUTA_VACACIONES} ")


    # calendario.csv
    if not os.path.exists(RUTA_CALENDARIO):

       with open("calendario.csv","w",newline="",encoding="utf-8") as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=[
                "fecha",
                "clase1",
                "clase2",
                "clase3"]
        )

        escritor.writeheader()

        fecha = datetime(2026, 1, 1)

        while fecha.year == 2026:

            escritor.writerow({

                "fecha":
                    fecha.strftime("%d/%m/%Y"),

                "clase1": 0,
                "clase2": 0,
                "clase3": 0
            })

            fecha += timedelta(days=1)

        registrar(f"Se creó {RUTA_CALENDARIO}")       

    guardar_registro_txt()


    empleados = cargar_csv(RUTA_EMPLEADOS)
    vacaciones = cargar_csv(RUTA_VACACIONES)
    calendario = cargar_csv(RUTA_CALENDARIO)

    

    return [empleados,vacaciones,calendario]

def validar_estructura_csv(csvs,columnas):
    Rutas=["empleados.csv",
          "vacaciones_2026.csv",
           "calendario.csv"]
   
    for ind, csv_x in enumerate(csvs):
        colunna = columnas[ind]
        ruta = Rutas[ind]
        
        
        if not csv_x:
            print(
                "\nERROR CRÍTICO"
                f"\nArchivo {ruta} vacío."
                "\nGestor de Vacaciones fuera de servicio.")
            registrar(f"Error critico: '{ruta} está vacío.'")
            guardar_registro_txt()
            return False

        columna_fila = list(csv_x[0].keys())
        if columna_fila != colunna:
            print(
                "\nERROR CRÍTICO"
                f"\nEstructura inválida en {ruta}'"
                "\nGestor de Vacaciones fuera de servicio.")
            registrar(f"Error critico. 'Estructura inválida en {ruta}'")
            guardar_registro_txt()
            return False
        
        for fila in csv_x:
            if not all(fila.values()):
                    print(
                    "\nERROR CRÍTICO"
                    f"\nEstructura corrupta en {ruta}'"
                    "\nGestor de Vacaciones fuera de servicio.")
                    registrar(f"Error critico. 'Estructura corrupta en {ruta}'")
                    guardar_registro_txt()
                    return
    return True




#Carga de registro.txt
def registrar(mensaje):

    fecha_hora = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    registro.append(
        f"[{fecha_hora}] {mensaje}"
    )

def guardar_registro_txt():

    global registro

    with open(RUTA_REGISTRO, "a", encoding="utf-8") as archivo:

        for linea in registro:
            archivo.write(linea + "\n")

    registro.clear()





##~~~Procesos~~~##
def validar_legajo():
    empleados = cargar_csv(RUTA_EMPLEADOS)
    vacaciones = cargar_csv(RUTA_VACACIONES)
    calendario = cargar_csv(RUTA_CALENDARIO)

    indice,empleado,legajo1 = buscar_legajo(empleados)


    if empleado == "gerente":
        if validar_contraseña("gerente", None):
            return "gerente","gerente",empleados, vacaciones, calendario
        return  "gerente",None, None, None , None

    else:
        registrar(f"-> ~~~~~~Ingreso legajo: {legajo1}~~~~~~")

        
        if indice is not None:
                
                if empleado["acceso"] == "False":  
                    print(f"\nLegajo {legajo1} acceso restringido. Comunicarse con administracion.\n")
                    registrar("Acceso restringido")
                    return None , indice, empleados, None , None

                if not validar_contraseña(indice, empleados):
                    empleados[indice]["acceso"] = "False"
                    guardar_csv(empleados, RUTA_EMPLEADOS)
                    print("Usuario bloqueado. Comunicarse con administracion para restableser la contraseña.\n")
                    registrar("Usuario bloquado. Max intentos")
                    
                    return None , indice, empleados, None , None
                    
                mostrar_empleado(indice,empleados)
                return  legajo1, indice, empleados, vacaciones, calendario 
        else:
            print(f"Legajo {legajo1} no encontrado\n")
            registrar("Legajo no encontrado") 
            return legajo1 ,None, empleados, None , None
            
def buscar_legajo(empleados):
    legajo = validar_numero("Ingrese su legajo: ")

    if legajo == id_gerente:
        return None,"gerente",None
    else:
        for indice,empleado in enumerate(empleados):
            if int(empleado["legajo"]) == legajo:
                return indice, empleado, legajo
        return None,None,legajo
        


def validar_contraseña(usuario,empleados):
    if usuario == "gerente":
        while True:
            if not contraseña_gerente == cifrar(input("Contraseña: ")):
                print("Volver a intentar?")
                if validar_menu(mostrar_menu_confirmacion, menu_confirmacion,):
                    continue
                else:
                    return False    
            return True 
               
    for i in range(3):
        
        if i > 0:
            print(f"Contraseña incorrecta. Quedan {3-i} intentos ")
            registrar(f"Contraseña incorrecta. Quedan {3-i} intentos ")
        contraseña = input("Contraseña: ")
        if empleados[usuario]["contraseña"] == cifrar(contraseña):
            return True
        
    return False    

def cambiar_contraseña(indice,empleados):
    registrar("Cambio de contraseña.")
    while True:
        nueva_contraseña = input("Nueva contraseña: ")
        if len(nueva_contraseña) < 6:
            print("Error. Contraseña tiene que tener mas de 6 caracteres.")
            registrar("Error. Contraseña menor a 6 caracteres.")
            continue
        nueva_contraseña2 = input("Repita contraseña: ")

        if nueva_contraseña == nueva_contraseña2:
            nueva_contraseña = cifrar(nueva_contraseña)
            if validar_menu(mostrar_menu_confirmacion, menu_confirmacion):
                empleados[indice]["contraseña"] = nueva_contraseña
                guardar_csv(empleados, RUTA_EMPLEADOS)
                print("Cambio exitoso.")
                registrar("Cambio exitoso.")
                break
            print("Volver a intentar?")
            if not validar_menu(mostrar_menu_confirmacion, menu_confirmacion):
                registrar("Cancelacion de cambio.")
                break
        else:
            print("La contraseña no coinciden, volver a intentar: ")  
            registrar("La contraseña no coincide.")
            if not validar_menu(mostrar_menu_confirmacion, menu_confirmacion):
                break
            registrar("Reintentar cambio de contraseña.")    

def mostrar_empleado(indice,empleados):
    print(f"\nNombre: {empleados[indice]["nombre"]}\n"
          f"Clase: {empleados[indice]["clase"]}\n"
          f"Antiguedad: {empleados[indice]["antiguedad"]}\n"
          f"Dias disponibles: {empleados[indice]["dias_disponibles"]}\n")
    registrar(f"Nombre: {empleados[indice]["nombre"]}\n"
        f"                      Clase: {empleados[indice]["clase"]}\n"
        f"                      Antiguedad: {empleados[indice]["antiguedad"]}\n"
        f"                      Dias disponibles: {empleados[indice]["dias_disponibles"]}")
   


#/// MENU EMPLEADOS
def menu_empleados(indice, empleados, vacaciones, calendario):
        if int(empleados[indice].get("dias_disponibles",0))== 0:
            op = validar_menu(mostrar_menu_s_dias,menu_s_dias)
        else:
            op = validar_menu(mostrar_menu_c_dias,menu_c_dias)    
             
    
        match op:
            case 1:
                solicitar_vacaciones(indice, empleados, vacaciones, calendario)
                
            case 2:
                consultar_historial_y_saldo(indice,empleados,vacaciones)

            case 3:
                 print("\nPara modificar una solicitud primero debe cancelarla y volver a solicitar.")
                 if validar_menu(mostrar_menu_confirmacion,menu_confirmacion):
                    cancelar_vacaciones(indice,empleados,vacaciones,calendario)
                
            case 0:
                return
                

#/// op 1 empleados
def solicitar_vacaciones(indice, empleados, vacaciones, calendario):
 
    empleado = empleados[indice]

    registrar(f"Inicio solicitud vacaciones ")


    dias_solicitados = validar_dias_solicitados(empleado)

    if dias_solicitados == None:
        registrar("Solicitud cancelada")
        return
    
    registrar(f"{dias_solicitados} solicitados.")

    fecha_inicio = pedir_fecha_inicio()

    registrar(f"{fecha_inicio} elegida.")


    fecha_fin = fecha_inicio + timedelta(days=dias_solicitados - 1)


    historial = obtener_historial_empleado(empleado["legajo"],vacaciones)

    if not validar_superposicion(historial,fecha_inicio,fecha_fin):
        return


    if not validar_cupo(empleado,fecha_inicio,fecha_fin,calendario,empleados):

        alternativa = sugerir_fechas(empleado,fecha_inicio,dias_solicitados,calendario,empleados)

        if alternativa is None:
            return

        fecha_inicio, fecha_fin = alternativa

    print(f"\nVacaciones aprobadas. Inicio: {fecha_inicio} Fin: {fecha_fin}\n")
    registrar(f"Fecha disponible: Inicio: {fecha_inicio.strftime("%d/%m/%Y")} Fin: {fecha_fin.strftime("%d/%m/%Y")}")
    
    if validar_menu(mostrar_menu_confirmacion,menu_confirmacion):
        registrar("Confirmada!")
        aprobar_solicitud(empleado,fecha_inicio,fecha_fin,dias_solicitados,empleados,indice,vacaciones,calendario)
    
    else:
        registrar("Rechazada!")

#/// op 2 empleados
def consultar_historial_y_saldo(indice,empleados,vacaciones):
    registrar("Consulta historial.")
    empleado = empleados[indice]

    print(f"\nSaldo disponible: {empleado['dias_disponibles']} días")

    historial = obtener_historial_empleado(empleado["legajo"],vacaciones)

    if not historial:

        print("\nNo posee solicitudes registradas.")
        registrar("No posee solicitudes registradas")

        return

    print("\nHistorial:")

    for vacacion in historial:

        print(
            f"\nInicio: {vacacion['fecha_inicio']}"
            f"\nFin: {vacacion['fecha_fin']}"
            f"\nDías: {vacacion['dias']}"
            f"\nEstado: {vacacion['estado']}" )
        registrar(f"Inicio: {vacacion['fecha_inicio']}\n"
            f"                       Fin: {vacacion['fecha_fin']}\n"
            f"                       Días: {vacacion['dias']}\n"
            f"                       Estado: {vacacion['estado']}\n" )
      
#/// op 3 empleados
def cancelar_vacaciones(indice,empleados,vacaciones,calendario,dias_previos=30):
    registrar("Inicio cancelacion de vacaciones.")

    empleado = empleados[indice]

    historial = obtener_historial_empleado(empleado["legajo"],vacaciones)

    aprobadas = []

    for vacacion in historial:

        if vacacion["estado"] == "Aprobada":

            aprobadas.append(vacacion)

    if not aprobadas:

        print("\nNo posee vacaciones aprobadas.")

        registrar("No posee vacaciones aprobadas.")

        return

    print("\nVacaciones aprobadas:\n")

    for i, vacacion in enumerate(aprobadas,start=1):

        print(
            f"{i}- "
            f"{vacacion['fecha_inicio']} al "
            f"{vacacion['fecha_fin']} "
            f"({vacacion['dias']} días)")

    print("0- Volver")

    opcion = validar_numero("\nSeleccione: ")

    if opcion == 0:
        return

    if opcion < 1 or opcion > len(aprobadas):

        print("Opción inválida.")
        return

    vacacion = aprobadas[opcion - 1]

    fecha_inicio = datetime.strptime(vacacion["fecha_inicio"],"%d/%m/%Y")

    if (fecha_inicio - datetime.now()).days < dias_previos:

        print(
            "\nLa cancelación debe realizarse "
            "con al menos 30 días de anticipación."
        )

        registrar(
            f"Cancelación rechazada "
            "menos de 30 días")

        return

   

    print("\n¿Desea cancelar la solicitud?\n")

    if not validar_menu(mostrar_menu_confirmacion,menu_confirmacion):

        return

    dias = int(vacacion["dias"])

    empleados[indice]["dias_disponibles"] = str(int(empleados[indice]["dias_disponibles"]) + dias)

    vacacion["estado"] = "Cancelada"

    fecha_fin = datetime.strptime(vacacion["fecha_fin"],"%d/%m/%Y")

    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:

        fecha_str = fecha_actual.strftime("%d/%m/%Y")

        for dia in calendario:

            if dia["fecha"] == fecha_str:

                columna = (f"clase{empleado['clase']}")

                dia[columna] = str(int(dia[columna]) - 1)

                break

        fecha_actual += timedelta(days=1)

    registrar(
        f"Vacaciones canceladas "
        f"{vacacion['fecha_inicio']} "
        f"{vacacion['fecha_fin']}")

    guardar_csv(empleados,RUTA_EMPLEADOS)

    guardar_csv(vacaciones,RUTA_VACACIONES)

    guardar_csv(calendario,RUTA_CALENDARIO)


    print("\nSolicitud cancelada correctamente.")



# /// fuciones op 1

def validar_dias_solicitados(empleado):
  
    dias_disponibles = int(empleado["dias_disponibles"])

    while True:
        print(f"Se sugiere soliciatar el total de {dias_disponibles} dias.\n")

        dias_solicitados = validar_numero("Cantidad de días: ")

        # pide más de lo disponible
        if dias_solicitados > dias_disponibles:

            registrar("Solicitud superior al saldo disponible")

            print(f"Solo dispone de {dias_disponibles} días.",
                   "Quiere volver a solicitar?\n")

            if not validar_menu(mostrar_menu_confirmacion, menu_confirmacion):
                return None

            continue

           # menos de 7
        if dias_solicitados < 7:
            print("No puede solicitar menos de 7 días.")
            registrar("No puede solicitar menos de 7 días.")
            continue  

        restante = dias_disponibles - dias_solicitados

        # regla del remanente
        if restante != 0 and restante < 7:
            print(f"No puede quedar menos de 7 días restantes.")
            registrar(f"No puede quedar menos de 7 días restantes.")

            sugerido = dias_disponibles - 7

            print(f"Se sugieren {sugerido} días.\n")
            registrar(f"Se sugieren {sugerido} días.")
            if validar_menu(mostrar_menu_confirmacion,menu_confirmacion):
                registrar("Solicitud aceptada.")
                return sugerido

            return None

        return dias_solicitados

def pedir_fecha_inicio():

    while True:

        fecha = input("\nFecha de inicio ""(DD/MM/AAAA): ").strip()

        try:

            fecha_inicio = datetime.strptime(fecha,"%d/%m/%Y")

        except ValueError:

            print("Fecha inválida.")
            registrar(f"Fecha invalida: {fecha}")


            continue
        
        fecha_minima = (datetime.now()+ timedelta(days=30))

        if fecha_inicio.date() < fecha_minima.date():

            print("\nLas vacaciones deben solicitarse con al menos 30 días de anticipación.\n")

            print(f"Fecha mínima: "
                  f"{fecha_minima.strftime('%d/%m/%Y')}")
            
            registrar("Fecha rechazada: 'Menor a 30 días de anticipación'")
            registrar(f"Fecha mínima: "
                      f"{fecha_minima.strftime('%d/%m/%Y')}")

            continue

        return fecha_inicio

def validar_cupo(empleado,fecha_inicio,fecha_fin,calendario,empleados):

    clase = empleado["clase"]

    porcentajes = {"1": 0.30,"2": 0.80,"3": 0.30}

    cantidad_clase = 0

    for emp in empleados:
        if emp["clase"] == clase:
            cantidad_clase += 1

    limite = max(1,int(cantidad_clase * porcentajes[clase]))

    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:

        fecha_str = fecha_actual.strftime("%d/%m/%Y")

        for dia in calendario:

            if dia["fecha"] == fecha_str:

                ocupacion = int(dia[f"clase{clase}"])

                if ocupacion >= limite:

                    registrar(f"Sin cupo clase {clase} "f"para {fecha_str}")

                    return False

                break

        fecha_actual += timedelta(days=1)

    return True

def sugerir_fechas(empleado,fecha_inicio,dias_solicitados,calendario,empleados):
    registrar("Sugerir fecha.")
    sugerencias = []

    fecha_prueba = fecha_inicio + timedelta(days=1)
    intentos = 0
    while len(sugerencias) < 2 and intentos < 365:
        intentos += 1

        fecha_fin =  fecha_prueba + timedelta(days=dias_solicitados - 1)

        if validar_cupo(empleado,fecha_prueba,fecha_fin,calendario,empleados):

            sugerencias.append((fecha_prueba,fecha_fin))

        fecha_prueba += timedelta(days=1)

    print("\nNo hay cupo para el período solicitado.")
    registrar("No hay cupo para el período solicitado.")

    for i, (inicio, fin) in enumerate(sugerencias, start=1):

        print(
            f"{i}- "
            f"{inicio.strftime('%d/%m/%Y')} "
            f"al "
            f"{fin.strftime('%d/%m/%Y')}")
        
    print(f"1- {sugerencias[0]}")
    print(f"2- {sugerencias[1]}")
    print( "0- Ingresar otra fecha")

    opcion = validar_menu([],menu_sugerencias)

    if opcion == 1:
        registrar(f"Acepta fecha alternativa {sugerencias[0]}")
        return sugerencias[0]
        
    if opcion == 2:
        registrar(f"Acepta fecha alternativa {sugerencias[1]}")
        return sugerencias[1]
    
    registrar(f"Rechaza fecha alternativa sugeridas")
    return None

def aprobar_solicitud(empleado,fecha_inicio,fecha_fin,dias_solicitados,empleados,indice,vacaciones,calendario):

    # Actualizar saldo

    dias_restantes = (int(empleado["dias_disponibles"])- dias_solicitados)

    empleados[indice]["dias_disponibles"] = str(dias_restantes)

    # Guardar histórico

    vacaciones.append({

        "legajo":empleado["legajo"],

        "fecha_solicitud":datetime.now().strftime("%d/%m/%Y"),

        "fecha_inicio":fecha_inicio.strftime("%d/%m/%Y"),

        "fecha_fin":fecha_fin.strftime("%d/%m/%Y"),

        "dias":str(dias_solicitados),

        "dias_restantes":str(dias_restantes),

        "estado":"Aprobada"
        })

    # Actualizar calendario

    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:

        fecha_str = fecha_actual.strftime("%d/%m/%Y")

        for dia in calendario:

            if dia["fecha"] == fecha_str:

                clase = (
                    f"clase"
                    f"{empleado['clase']}"
                )

                dia[clase] = str(int(dia[clase]) + 1)

                break

        fecha_actual += timedelta(days=1)

    registrar(
        f"Vacaciones registradas "
        f"{fecha_inicio.strftime('%d/%m/%Y')} "
        f"{fecha_fin.strftime('%d/%m/%Y')}")

    guardar_csv(empleados,RUTA_EMPLEADOS)

    guardar_csv(vacaciones,RUTA_VACACIONES)

    guardar_csv(calendario,RUTA_CALENDARIO)

    print("\nSolicitud aprobada.")
    registrar("Solicitud aprobada.")

    print(f"Saldo restante: "
          f"{dias_restantes} días.")




#/// funcion op 2 y "1"

def obtener_historial_empleado(legajo,vacaciones):

    historial = []

    for vacacion in vacaciones:

        if vacacion["legajo"] == legajo:

            historial.append(vacacion)

    return historial

def validar_superposicion(historial,fecha_inicio,fecha_fin):

    for vacacion in historial:

        if vacacion["estado"] != "Aprobada":
            continue

        inicio_existente = datetime.strptime(vacacion["fecha_inicio"],"%d/%m/%Y")

        fin_existente = datetime.strptime(vacacion["fecha_fin"],"%d/%m/%Y")

        if (fecha_inicio <= fin_existente and fecha_fin >= inicio_existente):

            print("\nYa posee vacaciones aprobadas que coinciden con ese período.")

            registrar("Solicitud rechazada: superposición de vacaciones.")

            return False

    return True



#// MENU ADMINISTRADOR

def menu_administrador(indice, empleados, vacaciones, calendario):

    while True:
        match validar_menu(mostrar_menu_admin,menu_admin):

            case 1:
                desbloquear_usuario(empleados)
            case 2:
                blanquear_acceso(empleados)
            case 3:
                listar_empleados(empleados)
            case 4:
                consultar_empleado(empleados,vacaciones)
            case 5:
                listar_vacaciones_aprobadas(vacaciones)
            case 6:
                cancelar_vacaciones_admin(empleados,vacaciones,calendario)
            case 7:
                print("Esta por CERRAR el 'Gestor de vacaciones'")
                if validar_menu(mostrar_menu_confirmacion,menu_confirmacion):
                    registrar("'Gestor de vacaciones' CERRADO")
                    guardar_registro_txt()
                    return True
            case 0:
                return False
        

#// op 1 admin
def desbloquear_usuario(empleados):

    registrar("Inicio desbloqueo de usuario.")

    indice,empleado,legajo = buscar_legajo(empleados)
    print("mira aca")
    print(indice)
    if indice is not None:

            if empleado["acceso"] == "True":

                print("\nEl usuario ya tiene acceso habilitado.")

                registrar(f"Intento de desbloqueo. Legajo {legajo} ya habilitado.")

                return

            print(f"\nEmpleado: {empleado['nombre']}")

            print("\n¿Confirmar desbloqueo?")

            if validar_menu(mostrar_menu_confirmacion,menu_confirmacion):

                empleado["acceso"] = "True"

                guardar_csv(empleados,RUTA_EMPLEADOS)

                print("\nUsuario desbloqueado.")

                registrar(
                    f"Usuario desbloqueado. Legajo {legajo}")

            else:

                registrar(f"Desbloqueo cancelado. Legajo {legajo}")

            return

    print("\nLegajo no encontrado.")

    registrar(
        f"Legajo no encontrado "
        f"en desbloqueo: {legajo}")

#// op 2 admin
def blanquear_acceso(empleados):

    registrar("Inicio blanqueo de acceso.")

    indice, empleado, legajo = buscar_legajo(empleados)

    if indice is None:

        print(f"\nLegajo {legajo} no encontrado.")

        registrar(
            f"Blanqueo cancelado. Legajo {legajo} no encontrado.")
        return

    nombre = normalizar(empleado["nombre"]).replace(" ", "")

    contraseña_temporal = (f"{nombre}{legajo}")

    print(f"\nEmpleado: {empleado['nombre']}"
          f"\nNueva contraseña: "
          f"{contraseña_temporal}")

    print("\nSe realizará:"
          "\n- Desbloqueo de acceso"
          "\n- Reinicio de contraseña")

    if not validar_menu(mostrar_menu_confirmacion,menu_confirmacion):

        registrar(f"Blanqueo cancelado. Legajo {legajo}")

        return

    empleados[indice]["acceso"] = "True"

    empleados[indice]["contraseña"] = cifrar(contraseña_temporal)

    guardar_csv(empleados,RUTA_EMPLEADOS)

    print("\nBlanqueo realizado correctamente.")

    registrar(f"Blanqueo realizado. Legajo {legajo}")

#// op 3 admin
def listar_empleados(empleados):

    registrar("Inicio listado de empleados")

    print("\n====== EMPLEADOS ======\n")

    for empleado in empleados:

        print(f"Legajo: {empleado['legajo']}"
             f"\nNombre: {empleado['nombre']}"
             f"\nClase: {empleado['clase']}"
             f"\nSaldo: {empleado['dias_disponibles']}"
             f"\nAcceso: {empleado['acceso']}"
             "\n")
            
    registrar("Listado de empleados finalizado")
    
#// op 4 admin
def consultar_empleado(empleados,vacaciones):

    registrar("Inicio consulta de empleado")

    indice, empleado, legajo = buscar_legajo(empleados)

    if indice is None:

        print(f"\nLegajo {legajo} no encontrado.")

        registrar(f"Consulta cancelada. Legajo {legajo} no encontrado")

        return

    mostrar_empleado(indice,empleados)

    historial = obtener_historial_empleado(empleado["legajo"],vacaciones)

    if historial:

        print("\nHistorial:\n")

        for vacacion in historial:

            print(f"\nInicio: {vacacion['fecha_inicio']}"
                  f"\nFin: {vacacion['fecha_fin']}"
                  f"\nDías: {vacacion['dias']}"
                  f"\nEstado: {vacacion['estado']}\n")
                

    registrar(f"Consulta realizada sobre legajo {legajo}")
        
#// op 5 admin
def listar_vacaciones_aprobadas(vacaciones):

    registrar("Inicio listado de vacaciones aprobadas")

    aprobadas = []

    for vacacion in vacaciones:

        if vacacion["estado"] == "Aprobada":

            aprobadas.append(vacacion)

    aprobadas.sort(key=lambda x:datetime.strptime(x["fecha_inicio"],"%d/%m/%Y"))

    print("\n====== VACACIONES APROBADAS ======\n")

    for vacacion in aprobadas:

        print(f"Legajo: {vacacion['legajo']}"
             f"\nInicio: {vacacion['fecha_inicio']}"
             f"\nFin: {vacacion['fecha_fin']}"
             f"\nDías: {vacacion['dias']}\n")
            

    registrar("Listado de vacaciones aprobado finalizado")

#// op 6 admin
def cancelar_vacaciones_admin(empleados,vacaciones,calendario):

    registrar("Inicio cancelación administrativa")

    indice, empleado, legajo = buscar_legajo(empleados)

    if indice is None:

        print(f"\nLegajo {legajo} no encontrado.")

        registrar(f"Cancelación administrativa. Legajo {legajo} no encontrado")

        return

    cancelar_vacaciones(indice,empleados,vacaciones,calendario,dias_previos=0)

    registrar(f"Cancelación administrativa ejecutada sobre {legajo}")




#/ MENU GERENTE

def menu_gerente(indice, empleados, vacaciones, calendario):
    cerrar_gestor = False
    while True:
        match validar_menu(mostrar_menu_gerente,menu_gerencia):

            case 1:
                consultar_empleado_gerente(empleados, vacaciones)
            case 2:
                estadisticas_generales(empleados, vacaciones)
            case 3:
                ver_calendario_vacaciones(calendario)
            case 4:
                 ver_registro_sistema()
            case 5:
                registrar("Gerente accedio a 'Administrador'")
                cerrar_gestor = menu_administrador(indice, empleados, vacaciones, calendario)
                registrar("Gerente salio de 'Administrador'")
                if cerrar_gestor:
                    break
            case 0:
                break
    return cerrar_gestor


#/ op 1 gerente
def consultar_empleado_gerente(empleados, vacaciones):

    registrar("Gerente inicio consulta de empleado")

    indice, empleado, legajo = buscar_legajo(empleados)

    if indice is None:

        print(f"\nLegajo {legajo} no encontrado.")

        registrar(f"Consulta gerente cancelada. Legajo {legajo} no encontrado")

        return

    mostrar_empleado(indice, empleados)

    historial = obtener_historial_empleado(empleado["legajo"],vacaciones)

    if historial:

        print("\nHistorial:\n")

        for v in historial:

            print(f"Inicio: {v['fecha_inicio']}"
                  f"\nFin: {v['fecha_fin']}"
                  f"\nDías: {v['dias']}"
                  f"\nEstado: {v['estado']}\n")
                

    registrar(f"Gerente consultó legajo {legajo}")

#/ op 2 gerente
def estadisticas_generales(empleados, vacaciones):

    registrar("Gerente inicio estadísticas generales")

    total_empleados = len(empleados)

    total_vacaciones = len(vacaciones)

    aprobadas = 0

    canceladas = 0

    for v in vacaciones:

        if v["estado"] == "Aprobada":
            aprobadas += 1

        elif v["estado"] == "Cancelada":
            canceladas += 1

    print("\n====== ESTADÍSTICAS ======\n")

    print(f"Empleados: {total_empleados}")
    print(f"Vacaciones registradas: {total_vacaciones}")
    print(f"Aprobadas: {aprobadas}")
    print(f"Canceladas: {canceladas}")

    registrar("Estadísticas generales generadas")

#/ op 3 gerente
def ver_calendario_vacaciones(calendario):

    registrar("Gerente visualiza calendario de vacaciones")

    print("\n====== CALENDARIO ======\n")

    for dia in calendario:

        print( f"{dia['fecha']} | "
               f"C1:{dia['clase1']} "
               f"C2:{dia['clase2']} "
               f"C3:{dia['clase3']}")
           

    registrar("Calendario mostrado")

#/ op 4 gerente

def ver_registro_sistema():

    meses_atras = validar_numero("Ver el registro de cuantos meses?: ")

    def restar_meses(fecha, meses):
        mes = fecha.month - meses
        año = fecha.year

        while mes <= 0:
            mes += 12
            año -= 1

        ultimo_dia = monthrange(año, mes)[1]
        dia = min(fecha.day, ultimo_dia)

        return fecha.replace(year=año, month=mes, day=dia)

    def ver_registro(meses_atras):

        if not 1 <= meses_atras <= 12:
            print("Rango inválido (1 a 12 meses)")
            return

        try:
            with open(RUTA_REGISTRO, "r", encoding="utf-8") as archivo:

                fecha_limite = restar_meses(datetime.now(),meses_atras)

                print("\n====== REGISTRO DEL SISTEMA ======\n")

                for linea in archivo:

                    try:
                        fecha_str = linea[1:20]
                        fecha_log = datetime.strptime(fecha_str,"%d/%m/%Y %H:%M:%S")

                    except ValueError:
                        continue

                    if fecha_log >= fecha_limite:
                        print(linea.strip())

        except FileNotFoundError:
            print("No hay registros.")

    ver_registro(meses_atras)





##~~~Limpiar_consola~~~##
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


def ___main___():
    ###-------------MAIN-------------###

    csv_ok= validar_estructura_csv(carga_inicial(),COLUMNAS_CSVC)
    arranque = True
    salir = False

    while not salir and csv_ok :
        
        time.sleep(4)
        limpiar_consola()

        if not arranque:
            if legajo != "gerente" :
                    registrar(f"-> ~~~~~~Fin legajo: {legajo}~~~~~~\n")
                    guardar_registro_txt()
        arranque = False




        print("\n====== GESTOR DE VACACIONES ======\n")

        # buscar legajo
        legajo,indice, empleados, vacaciones, calendario = validar_legajo()

        

        match indice:    
            case "gerente":
                salir = menu_gerente(indice, empleados, vacaciones, calendario)


            case 0:
                salir = menu_administrador(indice, empleados, vacaciones, calendario)
                

            
            case n if isinstance(n, int):
                menu_empleados(indice, empleados, vacaciones, calendario)
            
        
___main___()





def mostrar_logo():
    while True:
        Linea ="FUERA DE SERVICIO"
        separador= "----------"
        
        for letra in Linea:
            print(letra,separador,letra,separador,letra,separador,letra,separador,letra,separador,letra,separador,letra)
            time.sleep(0.4)
        print("\n\n")   
                   


        for _ in range(3):

            print("=" * 60)
            print(Linea.center(60))
            print("=" * 60)

            time.sleep(0.5)

            print(" " * 60)

            time.sleep(0.5)
        print("\n\n")    

mostrar_logo()
