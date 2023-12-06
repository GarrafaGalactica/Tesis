from apachelogs import LogParser, COMBINED
import csv
import re
import glob
import io
import pandas as pd

def armar_diccionario(list):
    dict = []
    for i in range(0,len(list)):
        with open(list[i], 'r') as file:
            expresiones = file.read().splitlines()
        for expresion in expresiones:
            if not expresion.startswith('^'):
                expresion = '.*'+expresion
            if not expresion.endswith('$'):
                expresion = expresion+'.*'
            dict.append(expresion)
    return dict
    


def match_expresiones_desde_archivo(cadena, dict):
    if cadena is None:
        return False
    for expresion in dict:
        if re.match(expresion, cadena):
            return True
    return False 


def buscar_ip(list):
    diccionario = dict()
    for i in range(0,len(list)):
        with open(list[i], 'r') as file:
            ips = file.read().splitlines()
        for ip in ips:
            if (ip != "") and (ip[0] != "#"):
                diccionario[ip] = True
    return diccionario 

parser = LogParser(COMBINED)
log_file_path = 'access-dspace.log.2'
#log_file_path = 'acces-chico'

csv_buffer = io.StringIO()

archivo_csv = "acces-log-test.csv"

l = 0

dict_ua = pd.DataFrame({"ua": armar_diccionario(glob.glob('spiders/agents/*'))})
#dict_ip = buscar_ip(glob.glob('spiders/*.txt'))
#dict_ip = pd.DataFrame({"ip": buscar_ip(glob.glob('spiders/*.txt'))})
dict_ip = buscar_ip(glob.glob('spiders/*.txt'))

csv_data = []

with open(log_file_path, 'r') as log_file:
        for line in log_file:
            entry = parser.parse(line)
            metodo = entry.request_line.split(" ")[0]
            recurso = entry.request_line.split(" ")[1]
            tiempo = entry.request_time
            #año = tiempo.year
            #mes = tiempo.month
            dateRaw = tiempo
            dia = tiempo.day
            hora = tiempo.hour
            minutos = tiempo.minute
            segundos = tiempo.second
            ip = entry.remote_host
            isBot = False
            UA = entry.headers_in["User-Agent"]
            if UA is None:
                UA = ""
            if ip in dict_ip:          
                    isBot = True
            else:
                ip_ar = ip.split(".")
                if ip_ar[0]+"."+ip_ar[1]+"."+ip_ar[2] in dict_ip:
                    isBot = True
                elif dict_ua['ua'].apply(lambda x: bool(re.search(x, UA))).any():
                    isBot = True
                else:
                    isBot = False
            status = entry.final_status
            csv_data.append([dateRaw, dia, hora, minutos, segundos, ip, metodo, recurso, status, UA, isBot])
            l+= 1
            print(l)

with open(archivo_csv, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Escribe la fila de encabezado
    writer.writerow(["dateRaw","dia", "hora","minuto","segundo","ip","metodo","recurso","codRespuesta","UserAgent","isBot"])
    writer.writerows(csv_data)
