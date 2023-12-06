import pandas as pd
import re

def procesar_valor(valor):
    arreglo = valor.split('/')
    if arreglo[1] == "handle":
        return "Vista"
    elif arreglo[1] == "bitstream":
        return "Descarga"
    elif arreglo[1] == "feed":
        return "Feed"
    elif arreglo[1] == "themes":
        return "Themes"
    elif arreglo[1] == "static":
        return "Static"
    elif arreglo[1] == "open-search":
        return "Open-Search"
    elif arreglo[1] == "":
        return "Home"
    elif re.match(r".*discover.*",arreglo[1]):
        return "Busqueda"
    elif re.match(r".*search-filter.*",arreglo[1]):
        return "Busqueda"
    elif re.match(r".*browse.*",arreglo[1]):
        return "Busqueda"
    elif re.match(r".*?id.*",arreglo[1]):
        return "Busqueda"
    elif arreglo[1] == "robots.txt":
        return "Robot"
    elif re.match(r".*robots.txt.*",arreglo[1]):
        return "Choices"
    elif arreglo[1] == "oai":
        return "Oai"
    elif arreglo[1] == "images":
        return "Images"
    elif arreglo[1] == "pages":
        return "Estaticas"
    elif arreglo[1] == "blog":
        return "Blog"
    elif re.match(r".*favicon.*",arreglo[1]):
        return "Icono"
    elif re.match(r".*apple-touch-icon.*",arreglo[1]):
        return "Icono"
    elif re.match(r".*wp-.*",arreglo[1]):
        return "WP"
    elif arreglo[1] == "password-login":
        return "Login"
    elif arreglo[1] == "login":
        return "Login"
    elif arreglo[1] == "forgot":
        return "Login"
    elif arreglo[1] == "admin":
        return "Admin"
    elif arreglo[1] == "register":
        return "Register"
    elif re.match(r".*register.*",arreglo[1]):
        return "Register"
    elif arreglo[1] == "profile":
        return "Profile"
    elif arreglo[1] == "community-list":
        return "Comunidades"
    elif arreglo[1] == "submissions":
        return "Submission"
    elif re.match(r".*submit.*",arreglo[1]):
        return "Submit"
    elif re.match(r".*js",arreglo[1]): 
        return "Javascript"
    elif re.match(r".*php",arreglo[1]):
        return "Php"
    elif re.match(r".*xml",arreglo[1]):
        return "Xml"
    elif re.match(r".*choices.*",arreglo[1]):
        return "Choices"
    elif re.match(r".*pdf",valor):
        return "Pdf"
    elif re.match(r"^\..*",arreglo[1]):
        return "Raro"
    elif arreglo[1] == "C":
        return "Raro"
    elif re.match(r".*etal.*",valor):
        return "Etal"
    elif re.match(r"^\?.*",arreglo[1]):
        return "Signo de pregunta"
    elif re.match(r".*sitemap.*",valor):
        return "Sitemap"
    elif arreglo[1] == "templates":
        return "Templates"
    elif arreglo[1] == "logout":
        return "Logout"
    elif arreglo[1] == "css":
        return "Css"
    elif re.match(r".*search.*",arreglo[1]):
        return "Search"
    elif re.match(r".*wlwmanifest.xml",valor):
        return "Wlwmanifest"
    elif arreglo[1] == "sites":
        return "Sites"
    elif arreglo[1] == "administrator":
        return "Administrator"
    else:
        return "Otro"


def listar(accesos):
    df = accesos
    while True:
        print("Menú:")
        print("0 - Filtrar por ip")
        print("1 - FIltrar por codigo de respuesta")
        print("2 - Filtrar por hora")
        print("3 - Filtrar por tipo")
        print("4 - Listar")

        # Pedir al usuario que ingrese una opción
        opcion = input("Selecciona una opción: ")

        if opcion == "0":
            ip = input("Elija una ip: ")
            df = df[df["ip"] == ip]
        elif opcion == "1":
            codigo = input("Elija un codigo de respuesta: ")
            df = df[df["codRespuesta"] == int(codigo)]
        elif opcion == "2":
            hora = input("Elija una hora: ")
            df = df[df["hora"] == int(hora)]
        elif opcion == "3":
            tipo = input("Elija un tipo de recurso: ")
            df = df[df["tipo"] == tipo]
        elif opcion == "4":
            print("Listando")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

    print(df)


def analizarFrecuencia(accesos):
    expresion_regular = r"^/themes.*"
    df_filtrado = accesos[accesos['isBot'] == False][~accesos['recurso'].str.contains(expresion_regular)][['ip','dateRaw']]
    count = df_filtrado.value_counts()
    ip_list = count[count > 9].index.to_list()
    #print(ip_list)

    # for row in ip_list:
    #     ip = row[0]
    #     #print(ip)
    #     accesos_ip = pd.Series()
    #     accesos_ip = accesos[accesos['isBot'] == False][accesos['ip'] == ip][['ip','dateRaw']]
    #     #print(accesos_ip)
    #     accesos_ip['dateRaw'] = pd.to_datetime(accesos_ip['dateRaw'])
    #     #print(accesos_ip.resample('T', on='dateRaw').count())
    #     #print(ip)
    #     break

def analizarRecurso(accesos):
    limite = int(input("Cual sera el limite: "))
    count = accesos[accesos['codRespuesta'] == 404][accesos['isBot'] == False]["ip"].value_counts()
    print(count[count > limite])
    ip_list_404 = count[count > limite].index.to_list()
    for row in ip_list_404:
        ip = row
        accesos_ip = pd.Series()
        accesos_ip = accesos[accesos['codRespuesta'] == 404][accesos['isBot'] == False][accesos['ip'] == ip][['ip','dateRaw']]
        accesos_ip['dateRaw'] = pd.to_datetime(accesos_ip['dateRaw'])
        print(accesos_ip.resample('T', on='dateRaw').count())
        print(ip)

# df_filtrado = accesos[accesos['isBot'] == False]
# conteo = df_filtrado['UserAgent'].value_counts()
# print(conteo[conteo > 100])

# ips = pd.DataFrame()
# ips[['1_octeto', '2_octeto', '3_octeto', '4_octeto']] = accesos['ip'].str.split('.', expand=True) #segun una tesis es la mejor manera
# #print(ips)

#expresion_regular = r".*\.js.*|.*\.css.*|.*\.png.*"
# accesos_duplicados = (
#     accesos[['hora', 'minuto', 'segundo', 'ip']]
#     .duplicated(keep=False)  # Detectar duplicados en las columnas 'hora', 'minuto', 'segundo' y 'ip'
#     &  # Operador lógico 'y'
#     ~accesos['recurso'].str.contains(expresion_regular, regex=True)  # Excluir las filas que coinciden con la expresión regular
# )
# print(accesos[accesos_duplicados]['ip'].value_counts())
# conteo = accesos[accesos_duplicados]['ip'].value_counts()
# conteo_mas_de_10 = conteo[conteo > 1]
# conteo

# print(conteo_mas_de_10)

# accesos['isGET'] = accesos['metodo'].apply(lambda x: 1 if x == 'GET' else 0)
# accesos['isPOST'] = accesos['metodo'].apply(lambda x: 1 if x == 'POST' else 0)
# accesos['isOTHER'] = accesos['metodo'].apply(lambda x: 1 if x != 'GET' and x != 'POST' else 0)
# accesos.drop(['metodo'], axis=1, inplace=True)
# filas_duplicadas = accesos.drop(['recurso'], axis=1, inplace=False).duplicated()
# #print(accesos[filas_duplicadas])

accesos = pd.read_csv("acces-log-bots.csv", encoding='ISO-8859-1')
accesos['tipo'] = accesos['recurso'].apply(procesar_valor)
aux = accesos[accesos["codRespuesta"] == 404]
print[aux[aux["tipo"] == "Vista"]]

while True:
    # Mostrar el menú
    print("Menú:")
    print("0 - Listar")
    print("1 - Analizar recurso")
    print("2 - Salir")

    # Pedir al usuario que ingrese una opción
    opcion = input("Selecciona una opción: ")

    # Verificar la opción seleccionada
    if opcion == "0":
        listar(accesos)
    elif opcion == "1":
        analizarRecurso(accesos)
    elif opcion == "2":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")