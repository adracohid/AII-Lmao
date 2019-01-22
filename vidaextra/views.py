from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from vidaextra.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from vidaextra.models import Noticia
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
    array = []
    for i in range(10):
        array.append(noticias[i + offset])
    return render(request, 'index.html', {'noticias': array})