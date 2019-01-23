

from bs4 import BeautifulSoup
import urllib.request,re
from datetime import datetime

def seleccionar_paginas():
    conjunto = set()
    for i in range(1,3):
        p = 'https://www.nintenderos.com/page/'+str(i)
        conjunto.add(p)
    return conjunto
def procesar_pagina(d:str):
    fichero=urllib.request.urlopen(d)
    documento=BeautifulSoup(fichero,"html.parser")
    return documento  
def extraer_titulo(e):
    return e.h3.a.text
def extraer_resumen(e):
    return e.p.text
def extraer_link(e):
    return e.h3.a['href']
def extraer_fecha(e):
    return e.footer.time.span.text
