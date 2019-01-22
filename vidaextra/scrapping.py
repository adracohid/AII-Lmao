from bs4 import BeautifulSoup
import urllib.request,re
from .models import Noticia

def procesar_pagina(d:str):
    fichero=urllib.request.urlopen(d)
    documento=BeautifulSoup(fichero,"html.parser")
    return documento


def extraer_titulo(e):
    return e.h2.a.string
def extraer_tipo(e):
    return e.find(class_="abstract-taxonomy").string
def extraer_resumen(e):
    return e.find(class_="abstract-excerpt").p.string
def extraer_link(e):
    return e.find(class_="abstract-link-more")['href']

def extraer_autor(e):
    if(e.find(class_="abstract-author")==None):
        return 'esta noticia no tiene autor'
    else:
        return e.find(class_="abstract-author").string
def extraer_fecha(e):
    return re.split('T',e.footer.time['titile'])[0]
def extraer_hora(e):
    return re.split('T',e.footer.time['titile'])[1][0:8]

def cargar():
    p=procesar_pagina("https://www.vidaextra.com/")

    l=p.find_all("div", class_=["abstract-content"])
    for e in l:
        titulo=extraer_titulo(e)
        resumen=extraer_resumen(e)
        link=extraer_link(e)
        autor=extraer_autor(e)
        fecha=extraer_fecha(e)
        hora=extraer_hora(e)
        print('Titulo: '+titulo +'\nResumen: '+resumen+ '\nLink: '+ link+ '\nAutor: '+ autor+ '\nFecha:' 
            + fecha + '\nHora: '+hora)
        noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
        noticia.save()
    