from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from vidaextra.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
<<<<<<< HEAD
from vidaextra.models import Noticia
from vidaextra import scrapping
=======
from vidaextra.models import Noticia, Puntuacion
from vidaextra.recomendation import predice_dos_noticias
>>>>>>> 800b2f2cb9d15e12790bc0328770f21d496818c0
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
    return HttpResponseRedirect("/login")

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
    array = []
    if(request.user.is_authenticated):
        extras = predice_dos_noticias(request.user.id)
    array.append(extras[0])
    array.append(extras[1])
    for i in range(10):
        array.append(noticias[i + offset])
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
    return render(request, 'index.html', {'noticias': array})

def puntua_noticia(request):
    punt = request.GET.get('puntuacion', 0)
    noticia = request.GET.get('noticia', 0)

    try:
        Puntuacion.objects.get(noticiaid = noticia, userid = request.user.id)
    except:
        puntuacion = Puntuacion(puntuacion = punt, noticiaid = noticia, userid = request.user.id)
        puntuacion.save()

    return HttpResponseRedirect("/")


def cargarvidaextra(request):
    p=scrapping.procesar_pagina("https://www.vidaextra.com/")

    l=p.find_all("div", class_=["abstract-content"])
    for e in l:
        titulo=scrapping.extraer_titulo(e)
        resumen=scrapping.extraer_resumen(e)
        link=scrapping.extraer_link(e)
        autor=scrapping.extraer_autor(e)
        fecha=scrapping.extraer_fecha(e)        
        noticia=Noticia(titulo=titulo,resumen=resumen,link=link,fecha=fecha)
        noticia.save()
    
    return HttpResponse("Loaded")