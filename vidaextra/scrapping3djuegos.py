from bs4 import BeautifulSoup
import urllib.request,re
from datetime import datetime

def seleccionar_paginas():
    conjunto = set()
    for i in range(0,2):
        p = 'https://www.3djuegos.com/#-portada_nov-'+str(i)+'f0f0f0'
        conjunto.add(p)
    return conjunto

def procesar_pagina(d:str):
    fichero=urllib.request.urlopen(d)
    documento=BeautifulSoup(fichero,"lxml")
    return documento
def extraer_titulo(e):
    return e.a.text

def extraer_resumen(e):
    return e.p.text

def extraer_link(e):
    return e.a['href']

def extraer_fecha(e):
    return e.find(class_="hace")['data-time']


paginas = seleccionar_paginas()
for pagina in paginas:
    p = procesar_pagina(pagina)
    l=p.find_all("div", class_=["nov_main_txt fftit"])
    for e in l:
        titulo=extraer_titulo(e)
        resumen=extraer_resumen(e)
        link=extraer_link(e)
        f=extraer_fecha(e)
        fecha = datetime.utcfromtimestamp(int(f)).strftime('%d/%m/%Y %H:%M:%S')
        
    
