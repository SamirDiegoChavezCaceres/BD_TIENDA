from django.shortcuts import render, redirect
from django.contrib.auth import forms  
from django.contrib import messages
from .forms import *;
import logging
loggerDjango = logging.getLogger('django')
loggerRequest = logging.getLogger('django.request')
loggerInventario = logging.getLogger('DBTienda')
loggerMenu = logging.getLogger('menuAndWelcome')
# Create your views here.
def inicioView(request, *args, **kwargs):
    #print(args, kwargs)
    #print(request.user)
    #https://stackoverflow.com/questions/2245895/is-there-a-simple-way-to-get-group-names-of-a-user-in-django#:~:text=You%20can%20get%20the%20groups,which%20will%20return%20a%20QuerySet%20.
    loggerMenu.info(f'{request.user.username} llego a pagina de inicio')
    return render(request, "inicio/home.html",{})

def licenciaView(request, *args, **kwargs):
    #print(args, kwargs)
    #print(request.user)
    loggerMenu.info(f'{request.user.username} llego a pagina de licencia')
    return render(request, "license/licencia.html",{})

#https://www.javatpoint.com/django-usercreationform
#https://learndjango.com/tutorials/django-login-and-logout-tutorial
def register(request):  
    form = CustomUserCreationForm()  
    if request.method == 'POST':  
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():  
            #print(form.cleaned_data)
            form.save()
            loggerMenu.info(f'{request.user.username} se creo el usuario {form.cleaned_data}')
        else:  
            #print(form.errors)
            loggerMenu.warning(f'{request.user.username} errores en la creacion de user {form.errors}')
    context = {  
        'form':form  
    }  
    return render(request, 'users/register.html', context)  