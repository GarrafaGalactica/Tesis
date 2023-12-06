import requests
import csv


# Realiza una solicitud GET a una URL que devuelve JSON
ventana = 3
i = ventana
años = 5
limite = 12 * años
while (i < limite):
    url = 'http://163.10.34.174:8080/solr_sedici/statistics/select?q=isBot%3AFalse&fq=time%3A%5BNOW-'+str(i)+'MONTH+TO+NOW-'+str(i - ventana)+'MONTH%5D&fq=statistics_type%3Aview&wt=json&indent=true&rows=1&wt=json&indent=true&facet=true&facet.field=ip&facet.limit=-1&facet.mincount=2000&facet.sort=count'
    response = requests.get(url)
    if response.status_code == 200:
        archivo_csv = "meses_accesos/"+str(i)+"-"+str(i - ventana)+".csv"
        with open(archivo_csv, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["ip", "cant"])
            ip = False
            cant = 0
            for line in response.json()['facet_counts']['facet_fields']['ip']:
                if isinstance(line, str):
                    ip = line
                else:
                    cant = line
                if isinstance(ip, str) and (cant > 0):
                    writer.writerow([ip,cant])
                    ip = False
                    cant = 0

    else:
        print(f'Error: {response.status_code}')
    
    i = i + ventana
