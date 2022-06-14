from django.shortcuts import render
from .models import *;
from .forms import *;

# Create your views here.
# control ventas / listar ver crear
def controlVentasView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    control = F2HControlVen.objects.get(convencod=kwargs['index'])
    boletas = V1TBoletaEleCab.objects.filter(bolelecabconvencod=kwargs['index'])
    pagos = F2TPagosControlVen.objects.filter(pagconvenconvencod=kwargs['index'])
    context = {
        'control': control,
        'boletas': boletas,
        'pagos': pagos,
    }
    print(context)
    return render(request, 'controlVentas/verControlVentas.html', context)

def listarControlVentasView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    controles = F2HControlVen.objects.all()
    context = {
        'controles': controles,
    }
    return render(request, 'controlVentas/listarControlVentas.html', context)

def crearControlVentasView(request, *args, **kwargs):
    form = RawControlVentasForm()
    if request.method == "POST":
        form = RawControlVentasForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            F2HControlVen.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    
    return render(request, 'controlVentas/crearControlVentas.html', context)

# compania / ver 
def companyView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = F2MCompany.objects.get(ciacod=kwargs['index'])
    context = {
        'codigo': obj.ciacod,
        'nombre': obj.cianom,
        'ruc': obj.ciaruc,
        'capital': obj.ciacap,
        'estado': obj.ciaestregcod.estregdes,
    }
    print(context)
    return render(request, 'company/verCompany.html', context)

# pagosConVen / ver crear
def pagoControlVentasView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = F2TPagosControlVen.objects.get(pagconvenconvencod=kwargs['index'])
    context = {
        'pagCodigo': obj.pagconvenpagcod,
        'trbCodigo': obj.pagconventrbcod,
        'year': obj.pagconvenfecaño,
        'mes': obj.pagconvenfecmes,
        'dia': obj.pagconvenfecdia,
        'hora': obj.pagconvenhor,
        'min': obj.pagconvenmin,
        'seg': obj.pagconvenseg,
        'estado': obj.pagconvenestregcod.estregdes,
    }
    print(context)
    return render(request, 'pagos/verPagosControlVentas.html', context)
    
def crearPagoControlVentasView(request, *args, **kwargs): //crear formulario
    form = RawControlVentasForm()
    if request.method == "POST":
        form = RawControlVentasForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            F2HControlVen.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    
    return render(request, 'pagos/crearPagosControlVentas.html', context)
# pagos / listar ver crear
def pagosView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    pago = F2TPagos.objects.get(pagcod=kwargs['index'])
    context = {
        'control': control,
        'boletas': boletas,
        'pagos': pagos,
    }
    print(context)
    return render(request, 'controlVentas/verControlVentas.html', context)

# boleta cab / ver crear

# boleta det / ver crear

# articulos / listar ver crear

# trabajador / listar ver crear

# transacciones / listar ver crear

# cliente / listar ver crear
