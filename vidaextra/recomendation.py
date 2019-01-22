from vidaextra.models import Puntuacion, Noticia
from django.contrib.auth.models import User
import math

def predice_dos_noticias(usuario):
    noticias = Noticia.objects.all()
    puntuaciones = Puntuacion.objects.filter(userid = usuario)
    
    noticias2 = []  
    for noticia in noticias:
        noticias2.append(noticia.id)
    
    puntuaciones2 = []
    for punt in puntuaciones:
        puntuaciones2.append(punt.noticiaid)
    
    comprobar = []
    for noticia in noticias2:
        if(noticia not in puntuaciones2):
            comprobar.append(noticia)
            
    lista = {}
    for noticia in comprobar:
        a = noticia
        b = predice(usuario, noticia)
        lista[a] = b
    
    primero = [None, None]
    segundo = [None, None]
    for noticia in lista:
        if(primero[0] is None):
            primero[0] = noticia
            primero[1] = lista[noticia]
        # Si no hay segundo
        elif (segundo[0] is None):
            segundo[0] = noticia
            segundo[1] = lista[noticia]
        # Si supera al primero
        elif(primero[1] < lista[noticia]):
            # Guarda el primero por si supera al segundo
            temp = [primero[0], primero[1]]
            primero[0] = noticia
            primero[1] = lista[noticia]
            if (temp[1] < segundo[1]):
                segundo[0] = temp[0]
                segundo[1] = temp[1]
        # Si supera al segundo
        elif(segundo[1] < lista[noticia]):
            segundo[0] = noticia
            segundo[1] = lista[noticia]
            
    return (primero, segundo)

# Devuelve lo similares que son dos usuarios (userids)
def similaridad(u1, u2):
    puntuaciones_1 = Puntuacion.objects.filter(userid = u1)
    puntuaciones_2 = Puntuacion.objects.filter(userid = u2)
    
    # Guarda los noticias de u1
    noticias_1 = []
    for punt in puntuaciones_1:
        noticias_1.append(punt.noticiaid)
        
    # Guarda los noticias de u2
    noticias_2 = []
    for punt in puntuaciones_2:
        noticias_2.append(punt.noticiaid)
    
    # Guarda los noticias de los cuales ambos tienen puntuaciones
    comunes = []
    for noticia in noticias_1:
        if(noticia in noticias_2):
            comunes.append(noticia)
            
            
    # Puntuaciones medias de los usuarios
    media_1 = puntuacion_media_usuario(u1)
    media_2 = puntuacion_media_usuario(u2)
    
    
    # Calcula la similitud
    arriba = 0
    for comun in comunes:
        a = Puntuacion.objects.get(userid = u1, noticiaid = comun).puntuacion - media_1
        b = Puntuacion.objects.get(userid = u2, noticiaid = comun).puntuacion - media_2
        arriba = arriba + a*b
    
    abajo_1 = 0
    for comun in comunes:
        c = Puntuacion.objects.get(userid = u1, noticiaid = comun).puntuacion - media_1
        c = c * c
        abajo_1 = abajo_1 + c
    abajo_1 = math.sqrt(abajo_1)
    
    abajo_2 = 0
    for comun in comunes:
        c = Puntuacion.objects.get(userid = u2, noticiaid = comun).puntuacion - media_2
        c = c * c
        abajo_2 = abajo_2 + c
    abajo_2 = math.sqrt(abajo_2)
    
    if (abajo_1 * abajo_2 > 0):
        return arriba / (abajo_1 * abajo_2)
    else:
        return arriba

def predice(usuario, noticia):
    media_usuario = puntuacion_media_usuario(usuario)
    
    usuarios_bd1 = User.objects.all()
    usuarios_bd = []
    for i in usuarios_bd1:
        usuarios_bd.append(i.id)
    
    arriba = 0
    abajo = 0
    for otro_usuario in usuarios_bd:
        a = similaridad(usuario, otro_usuario) 
        abajo = abajo + similaridad(usuario, otro_usuario)
        try:
            punt_uacion = Puntuacion.objects.get(userid = otro_usuario, noticiaid = noticia) - puntuacion_media_usuario(otro_usuario)
        except:
            continue
        a = a * (punt_uacion - puntuacion_media_usuario(otro_usuario))
        arriba = arriba + a
        
    if(abajo == 0):
        abajo = 1
    return (arriba / abajo) + media_usuario
    
    
    
def puntuacion_media_usuario(usuario):
    puntuaciones_usuario = Puntuacion.objects.filter(userid = usuario)
    
    media_usuario = 0
    for punt in puntuaciones_usuario:
        media_usuario = media_usuario + punt.puntuacion
    if(len(puntuaciones_usuario) > 0):
        media_usuario = media_usuario / len(puntuaciones_usuario)
    else:
        media_usuario = media_usuario / 1

    return media_usuario