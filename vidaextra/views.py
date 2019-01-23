from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from vidaextra.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from vidaextra import scrapping,scrapping3djuegos,scrappinglevelup,scrapinnintenderos
from vidaextra.models import Noticia, Puntuacion
from vidaextra.recomendation import predice_dos_noticias
import random
from datetime import datetime
# Create your views here.

def login_view(request):
    if (request.user.is_authenticated):
        logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password = form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render(request, 'login.html', {'form': form, "error": "Invalid credentials"})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if (request.user.is_authenticated):
        logout(request)
    return HttpResponseRedirect("/")

def register_view(request):
    if (request.user.is_authenticated):
        logout(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirmpassword = form.cleaned_data["confirmpassword"]
            email = form.cleaned_data["email"]
            
            # Check data
            if(password != confirmpassword):
                return render(request, 'register.html', {'form': form, "error": "Passwords don't match"})
            try:
                u1 = User.objects.get(username = username)
                if u1 is not None:
                    return render(request, 'register.html', {'form': form, "error": "That username is already taken"})
            except:
                pass
            try:
                u2 = User.objects.get(email = email)
                if u2 is not None:
                    return render(request, 'register.html', {'form': form, "error": "That email is already taken"})
            except:
                pass
            # Create user
            newuser = User.objects.create_user(username, email, password)
            newuser.save()
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render(request, 'register.html', {'form': form, "error": "Invalid credentials"})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def index_view(request):
    offset = request.GET.get('p', 0)
    noticias = Noticia.objects.all()
    if(len(noticias) == 0):
        return HttpResponse("Nothing to display")
    offset = int(offset)
    nextpag = offset + 10
    prevpag = offset - 10
    while(offset > len(noticias) - 10):
        nextpag = None
        offset = offset - 10
    
    array = []
    recomendadas = []
    if(request.user.is_authenticated and len(Puntuacion.objects.all()) >= 5):
        extras = predice_dos_noticias(request.user.id)
        puntuada1 = False
        extra1 = Noticia.objects.get(id = extras[0][0])
        extra2 = Noticia.objects.get(id = extras[1][0])
        try:
            Puntuacion.objects.get(noticiaid = extra1.id, userid = request.user.id)
            puntuada1 = True
        except:
            pass
        dic1 = {
            "titulo": extra1.titulo,
            "resumen": extra1.resumen,
            "link": extra1.link,
            "puntuada": puntuada1,
            "id": extra1.id
        }
        puntuada2 = False
        try:
            Puntuacion.objects.get(noticiaid = extra2.id, userid = request.user.id)
            puntuada2 = True
        except:
            pass
        dic2 = {
            "titulo": extra2.titulo,
            "resumen": extra2.resumen,
            "link": extra2.link,
            "puntuada": puntuada2,
            "id": extra2.id
        }
        recomendadas.append(dic1)
        recomendadas.append(dic2)
    for i in range(10):
        puntuada = False
        try:
            Puntuacion.objects.get(noticiaid = noticias[i + offset].id, userid = request.user.id)
            puntuada = True
        except:
            pass
        dic = {
            "titulo": noticias[i + offset].titulo,
            "resumen": noticias[i + offset].resumen,
            "link": noticias[i + offset].link,
            "puntuada": puntuada,
            "id": noticias[i + offset].id
        }
        array.append(dic)
    return render(request, 'index.html', {'noticias': array,'recomendadas': recomendadas, 'pag': offset, 'prevpag': prevpag, 'nextpag': nextpag})

def puntua_noticia(request):
    punt = request.GET.get('puntuacion', 1)
    noticia = request.GET.get('noticia', 0)
    punt = int(punt)
    if(punt > 5):
        punt = 5
    if (punt < 1):
        punt = 1
    if (not request.user.is_authenticated):
        return HttpResponseRedirect("/")
    try:
        Puntuacion.objects.get(noticiaid = noticia, userid = request.user.id)
    except:
        puntuacion = Puntuacion(puntuacion = punt, noticiaid = noticia, userid = request.user.id)
        puntuacion.save()

    return HttpResponseRedirect("/")


def haz_scraping(request):
    # Tira la BD
    Noticia.objects.all().delete()
    Puntuacion.objects.all().delete()
    User.objects.all().delete()

    # Crea usuarios de prueba
    for i in range(10):
        newuser = User.objects.create_user("test" + str(i), "test" + str(i)+"@gmail.com", "test" + str(i))
        newuser.save()
    #scraping 3djuegos
    try:

        cargar3djuegos(request)
        status_pagina1="Pagina https://www.3djuegos.com cargada con exito"
    except:
        status_pagina1="Error al cargar la pagina https://www.3djuegos.com"
    #scraping vidaextra
    try:
        
        cargarvidaextra(request)
        status_pagina2="Pagina https://www.vidaextra.com/ cargada con exito"
    except:
        status_pagina2="Error al cargar la pagina https://www.vidaextra.com/"
    
    #scraping levelup
    try:
        cargarlevelup(request)
        status_pagina3="Pagina https://www.levelup.com/noticias cargada con exito"

    except:
        status_pagina3="Error al cargar la pagina https://www.levelup.com/noticias"

    #Scraping nintenderos
    try:
        cargarnintenderos(request)
        status_pagina4="Pagina https://www.nintenderos.com/ cargada con exito"
    except:
        status_pagina4="Error al cargar la pagina https://www.nintenderos.com/"
    # Crea puntuaciones de prueba
    try:

        for i in range(10):
            usuario = User.objects.get(username="test"+str(i))
            for j in range(5):
                noticiaid = random.randint(1, len(Noticia.objects.all()) - 1)
                try:
                    Puntuacion.objects.get(noticiaid = noticiaid, puntuacion = 5, userid = usuario.id)
                except:
                    punt = Puntuacion(noticiaid = noticiaid, puntuacion = 5, userid = usuario.id)
                    punt.save()
        error=" "
    except:
        #En el caso de que no se cargara ninguna pagina 
        error="No se ha podido cargar ninguna noticia"
    return render(request,'request.html',context={'status_pagina1':status_pagina1,'status_pagina2':status_pagina2,'status_pagina3':status_pagina3,'status_pagina4':status_pagina4,'error':error})

def cargar3djuegos(request):
    paginas = scrapping3djuegos.seleccionar_paginas()
        
    for pagina in paginas:
        p = scrapping3djuegos.procesar_pagina(pagina)
        l=p.find_all("div", class_=["nov_main_txt fftit"])
        for e in l:
            titulo=scrapping3djuegos.extraer_titulo(e)
            resumen=scrapping3djuegos.extraer_resumen(e)
            link=scrapping3djuegos.extraer_link(e)
            f=scrapping3djuegos.extraer_fecha(e)
            fecha = datetime.utcfromtimestamp(int(f)).strftime('%d/%m/%Y %H:%M:%S')
            noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
            noticia.save()


def cargarvidaextra(request):
    p=scrapping.procesar_pagina("https://www.vidaextra.com/")
    l=p.find_all("div", class_=["abstract-content"])
    for e in l:
        titulo=scrapping.extraer_titulo(e)
        resumen=scrapping.extraer_resumen(e)
        link=scrapping.extraer_link(e)
        fecha=scrapping.extraer_fecha(e)+' '+scrapping.extraer_hora(e)      
        noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
        noticia.save()

def cargarlevelup(request):
    l=scrappinglevelup.procesar_pagina()
    for e in l:
        titulo=scrappinglevelup.extraer_titulo(e)
        resumen=scrappinglevelup.extraer_resumen(e)
        link=scrappinglevelup.extraer_link(e)
        fecha=scrappinglevelup.extraer_fecha(e)
        noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
        noticia.save()

def cargarnintenderos(request):
    p=scrapinnintenderos.procesar_pagina('https://www.nintenderos.com/')
    l=p.find_all("div", class_=["c-post-list__content"])
    for e in l:
        titulo=scrapinnintenderos.extraer_titulo(e)
        resumen=scrapinnintenderos.extraer_resumen(e)
        link=scrapinnintenderos.extraer_link(e)
        fecha='Hace '+ scrapinnintenderos.extraer_fecha(e)
        noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
        noticia.save()
