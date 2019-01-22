from bs4 import BeautifulSoup
import urllib.request,re
from datetime import datetime
import ssl 

def procesar_pagina():
    f = urllib.request.urlopen("https://www.levelup.com/noticias", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    s = BeautifulSoup(f,"lxml")
    l = s.find_all("article", class_= ["cf news"])
    
    return l

def extraer_titulo(e):
    titulo = e.find("a", class_="rC")['title']
    titulo = re.sub('<em>', '', titulo)
    titulo = re.sub('</em>', '', titulo)
    return titulo

def extraer_resumen(e):
    return e.find("p", class_="elementIntro").text

def extraer_link(e):
    link = e.find("a", class_="rC")['href']
    link = "https://www.levelup.com" + link
    return link

def extraer_fecha(e):
    fecha = e.find("p", class_="time").time['data-timestamp']
    fecha = datetime.utcfromtimestamp(int(fecha)).strftime('%d/%m/%Y %H:%M:%S')
    return fecha


l = procesar_pagina()

for e in l:
    titulo=extraer_titulo(e)
    resumen=extraer_resumen(e)
    link=extraer_link(e)
    fecha=extraer_fecha(e)
    print('Titulo: '+titulo+ '\n Resumen: '+resumen+ '\n Link: '+link+ '\n Fecha: '+ fecha)
    