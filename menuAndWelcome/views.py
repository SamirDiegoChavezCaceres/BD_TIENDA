from django.shortcuts import render

# Create your views here.
def inicioView(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "inicio/home.html",{})

def licenciaView(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "license/licencia.html",{})