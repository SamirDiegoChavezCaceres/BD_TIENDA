from decimal import Decimal
from django.shortcuts import render
from .models import *;
from .forms import *;
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.
# control ventas / listar ver crear

def controlVentasCapital(**kwargs):
    control = F2HControlVen.objects.get(convencod=kwargs['index'])
    company = control.convenciacod
    montoAntiguo = kwargs['montoAntiguo']
    montoNuevo = kwargs['montoNuevo']
    balance = montoNuevo - montoAntiguo

    balance = control.convencapfin + balance
    capciaFin = company.ciacap + balance

    F2HControlVen.objects.filter(convencod=kwargs['index']).update(convencapfin=(control.convencapini-balance))
    F2MCompany.objects.filter(ciacod=control.convenciacod.ciacod).update(ciacap=capciaFin)

def impresionView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
    }
    print(context)

    return render(request, 'imprimir/tabla.html', context)

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

def crearControlVentasView(request):
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
    obj = F2TPagosControlVen.objects.get(pagconvencod=kwargs['index'])
    context = {
        'pagCodigo': obj.pagconvenpagcod,
        'trbCodigo': obj.pagconventrbcod,
        'year': obj.pagconvenfecaño,
        'mes': obj.pagconvenfecmes,
        'dia': obj.pagconvenfecdia,
        'hora': obj.pagconvenhor,
        'min': obj.pagconvenmin,
        'seg': obj.pagconvenseg,
        'estado': obj.pagconvenestregcod,
    }
    print(context)
    return render(request, 'pagos/verPagosControlVentas.html', context)
    
def crearPagoControlVentasView(request, *args, **kwargs): 
    comp = F2MCompany.objects.get(ciacod=1) 
    estado = GzzEstadoRegistro.objects.get(estregcod='A')

    controlven, created = F2HControlVen.objects.get_or_create(
        convenfecaño=time.localtime(time.time()).tm_year,
        convenfecmes=time.localtime(time.time()).tm_mon,
        convenfecdia=time.localtime(time.time()).tm_mday,
        defaults={'convenciacod': comp, 'convencapini': comp.ciacap, 'convencapfin': 0, 'convenestregcod': estado},
    )
    if(created):
        print("Created!")

    trabajador = R1MTrabajador.objects.get(trartt=1)
    pago = F2TPagos.objects.get(pagcod=kwargs['indexPago']) 

    initial_dict = {
        "pagconvenconvencod" : controlven,
        "pagconvenpagcod" : pago,
        "pagconventrbcod" : trabajador,
        "pagconvenfecaño" : time.localtime(time.time()).tm_year,
        "pagconvenfecmes" : time.localtime(time.time()).tm_mon,
        "pagconvenfecdia" : time.localtime(time.time()).tm_mday,
        "pagconvenhor" : time.localtime(time.time()).tm_hour,
        "pagconvenmin" : time.localtime(time.time()).tm_min,
        "pagconvenseg" : time.localtime(time.time()).tm_sec,
        "pagconvenestregcod" : "",
    }
    form = RawPagosControlVentasForm(initial=initial_dict)
    if request.method == "POST":
        form = RawPagosControlVentasForm(request.POST)
        form.fields['pagconvenconvencod'].initial = initial_dict['pagconvenconvencod']
        form.fields['pagconvenpagcod'].initial = initial_dict['pagconvenpagcod']
        form.fields['pagconventrbcod'].initial = initial_dict['pagconventrbcod']
        if form.is_valid():
            print(form.cleaned_data)
            pagoControl = F2TPagosControlVen.objects.create(**form.cleaned_data)
            company = F2MCompany.objects.get(ciacod=controlven.convenciacod.ciacod)

            capFin = controlven.convencapfin - pagoControl.pagconvenpagcod.pagpre
            capciaFin = company.ciacap - pagoControl.pagconvenpagcod.pagpre

            F2HControlVen.objects.filter(convencod=controlven.convencod).update(convencapfin=capFin)
            F2MCompany.objects.filter(ciacod=controlven.convenciacod.ciacod).update(ciacap=capciaFin)
        else:
            print(form.errors)
    context = {
        'form': form,
    }

    rendered = render_to_string('pagos/crearPagosControlVentas.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

# pagos / listar ver crear update delete
def pagosView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    pago = F2TPagos.objects.get(pagcod=kwargs['index'])
    context = {
        'codigo': pago.pagcod,
        'nombre': pago.pagnom,
        'descripcion': pago.pagdsc,
        'precio': pago.pagpre,
        'estado': pago.pagestregcod,
    }
    print(context)
    return render(request, 'pagos/verPago.html', context)

def listarPagosView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    pagos = F2TPagos.objects.all()
    context = {
        'pagos': pagos,
    }
    return render(request, 'pagos/listarPagos.html', context)

def crearPagosView(request):
    form = RawPagosForm()
    if request.method == "POST":
        form = RawPagosForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            F2TPagos.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    return render(request, 'pagos/crearPagos.html', context)
# boleta cab / ver crear 
def boletaCabeceraFinalView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=kwargs['index'])
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=kwargs['index'])
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
    }
    print(context)
    return render(request, 'boleta/verBoletaCabFin.html', context)
    
def boletaCabeceraFinalEstView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=kwargs['index'])
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=kwargs['index'])
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)
    return render(request, 'boleta/crearBoletaCab.html', context)

def crearBoletaCabeceraView(request, *args, **kwargs):
    comp = F2MCompany.objects.get(ciacod=1)
    estado = GzzEstadoRegistro.objects.get(estregcod='A')

    controlven, created = F2HControlVen.objects.get_or_create(
        convenfecaño=time.localtime(time.time()).tm_year,
        convenfecmes=time.localtime(time.time()).tm_mon,
        convenfecdia=time.localtime(time.time()).tm_mday,
        defaults={'convenciacod': comp, 'convencapini': comp.ciacap, 'convencapfin': 0, 'convenestregcod': estado},
    )
    trabajador = R1MTrabajador.objects.get(trartt=1)
    if kwargs['dni'] != 0:
        cliente, created = V2MCliente.objects.get_or_create(
            clinom=kwargs['nombre'],
            clidni=kwargs['dni'],
            defaults={'cliestregcod': estado},
        )
    else:
        cliente, created = V2MCliente.objects.get_or_create(
            clinom=kwargs['nombre'],
            clidni=0,
            defaults={'cliestregcod': estado},
        )

    initial_dict = {
        "bolelecabconvencod" : controlven,
        "bolelecabfecaño" : time.localtime(time.time()).tm_year,
        "bolelecabfecmes" : time.localtime(time.time()).tm_mon,
        "bolelecabfecdia" : time.localtime(time.time()).tm_mday,
        "bolelecabhor" : time.localtime(time.time()).tm_hour,
        "bolelecabmin" : time.localtime(time.time()).tm_min,
        "bolelecabseg" : time.localtime(time.time()).tm_sec,
        "bolelecabclicod" : cliente,
        "bolelecabtrbcod" : trabajador,
        "bolelecabtot" : 0,
        "bolelecabestregcod" : estado,
    }
    bolCab = V1TBoletaEleCab.objects.create(**initial_dict)
    
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=bolCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=bolCab.bolelecabcod)
    context = {
        'boletaCab': bolCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

# boleta det / crear update delete
def crearBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
        boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
        boleledettraestregcod=estado,
        defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00,},
    )
    
    

    transaccion = V1TTransaccion.objects.get(tracod=boletaDet.boleledettratracod.tracod)
    importeAntiguo = Decimal(boletaDet.boleledettratraimp)
    importeNuevo = Decimal(boletaDet.boleledettratraimp)+Decimal(transaccion.trapre)

    V1TBoletaEleDetTra.objects.filter(boletadettracod=boletaDet.boletadettracod).update(
                                                                    boleledettratracan=(boletaDet.boleledettratracan+1),
                                                                    boleledettratraimp=importeNuevo,
                                                                    )
    """ setattr(boletaDet, "boleledettratracan", (boletaDet.boleledettratracan+1))
    setattr(boletaDet, "boleledettratraimp", (importeNuevo))
    boletaDet.save() """


    boletaCab = boletaDet.boleledettrabolelecabcod
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

    
    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
                                                                    bolelecabtot=(boletaCab.bolelecabtot+transaccion.trapre),
                                                                    )
    """ setattr(boletaCab, "bolelecabtot", (boletaCab.bolelecabtot+transaccion.trapre))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaCab.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)
    
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }

    
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

def updateBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
        boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
        defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00, 'boleledettraestregcod': estado},
    )
    importeAntiguo = Decimal(boletaDet.boleledettratraimp)
    importeNuevo = Decimal(kwargs['cantidad']*boletaDet.boleledettratracod.trapre)

    V1TBoletaEleDetTra.objects.filter(boletadettracod=boletaDet.boletadettracod).update(
                                                                    boleledettratracan=(kwargs['cantidad']),
                                                                    boleledettratraimp=importeNuevo,
                                                                    )
    """ setattr(boletaDet, "boleledettratracan", (kwargs['cantidad']))
    setattr(boletaDet, "boleledettratraimp", (importeNuevo))
    boletaDet.save() """

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledettrabolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
   
    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
                                                                    bolelecabtot=(totalNuevo),
                                                                    )
    """ setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledettrabolelecabcod.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)

    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

def deleteBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
        boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
        defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00, 'boleledettraestregcod': estado},
    )
    importeAntiguo = Decimal(boletaDet.boleledettratraimp)
    importeNuevo = 0
    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    V1TBoletaEleDetTra.objects.filter(boletadettracod=boletaDet.boletadettracod).update(
                                                                    boleledettraestregcod=estado,
                                                                    )
    """ setattr(boletaDet, "boleledettraestregcod", estado)
    boletaDet.save() """

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledettrabolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo) 

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
                                                                    bolelecabtot=(totalNuevo),
                                                                    )
    """  setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledettrabolelecabcod.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)

    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response
#//////////////////////////
def crearBoletaDetArtView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    if kwargs['indexArt'] < 1000000000000:
        boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcod=kwargs['indexArt']),
        boleledetartestreg=estado,
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00,},
        )
    else:
        boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcodbar=kwargs['indexArt']),
        boleledetartestreg=estado,
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00,},
        )
    
    
    producto = L1MArticulo.objects.get(artcod=boletaDet.boleledetartartcodbar.artcod)

    importeAntiguo = Decimal(boletaDet.boleledetartartimp)
    importeNuevo = Decimal(boletaDet.boleledetartartimp)+producto.artpreuni

    V1TBoletaEleDetArt.objects.filter(boleledetartcod=boletaDet.boleledetartcod).update(
        boleledetartartcan=(boletaDet.boleledetartartcan+1),
        boleledetartartimp=(importeNuevo),
    )
    L1MArticulo.objects.filter(artcod=boletaDet.boleledetartartcodbar.artcod).update(
        artstk=(boletaDet.boleledetartartcodbar.artstk-1)
        )
    """ setattr(boletaDet, "boleledetartartcan", (boletaDet.boleledetartartcan+1))
    setattr(boletaDet, "boleledetartartimp", (importeNuevo))
    setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-1))
    boletaDet.save()
    boletaDet.boleledetartartcodbar.save() """


    boletaCab = boletaDet.boleledetartbolelecabcod
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
        bolelecabtot=(totalNuevo),
        )
    """ setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaCab.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)
    
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

def updateBoletaDetArtView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcod=kwargs['indexArt']),
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00, 'boleledetartestreg': estado},
    )
    cantidadAnt = boletaDet.boleledetartartcan
    cantidadNue = kwargs['cantidad']
    
    importeAntiguo = Decimal(boletaDet.boleledetartartimp)
    importeNuevo = Decimal(cantidadNue*boletaDet.boleledetartartcod.artpreuni)


    V1TBoletaEleDetArt.objects.filter(boleledetartcod=boletaDet.boleledetartcod).update(
        boleledetartartcan=(cantidadNue),
        boleledetartartimp=(importeNuevo),
        )
    L1MArticulo.objects.filter(artcod=boletaDet.boleledetartartcodbar.artcod).update(
        artstk= (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt))
        )
    
    """ setattr(boletaDet, "boleledetartartcan", (cantidadNue))
    setattr(boletaDet, "boleledetartartimp", (importeNuevo))
    setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt)))
    boletaDet.save()
    boletaDet.boleledetartartcodbar.save() """

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
        bolelecabtot=(totalNuevo),
        )
    """ setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save()
     """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)

    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response

def deleteBoletaDetArtView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcod=kwargs['indexArt']),
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00, 'boleledetartestreg': estado},
    )
    cantidadAnt = boletaDet.boleledetartartcan
    cantidadNue = 0
    
    importeAntiguo = Decimal(boletaDet.boleledetartartimp)
    importeNuevo = Decimal(cantidadNue*boletaDet.boleledetartartcodbar.artpreuni)

    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    V1TBoletaEleDetArt.objects.filter(boleledetartcod=boletaDet.boleledetartcod).update(
        boleledetartestreg=(estado),
        )
    L1MArticulo.objects.filter(artcod=boletaDet.boleledetartartcodbar.artcod).update(
        artstk= (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt))
        )
    """ setattr(boletaDet, "boleledettraestregcod", estado)
    setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt)))
    boletaDet.save()
    boletaDet.boleledetartartcodbar.save() """

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
    
    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)
    
    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
        bolelecabtot=(totalNuevo),
        )
    """ setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)

    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    print(rendered)
    response = JsonResponse(rendered, safe=False)
    print(response)
    return response
# articulos / listar ver crear update delete
def articulosView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = L1MArticulo.objects.get(artcod=kwargs['index'])
    context = {
        'codigo': obj.artcodbar,
        'nombre': obj.artnom,
        'desc': obj.artdsc,
        'precio': obj.artpreuni,
        'stock': obj.artstk,
        'estado': obj.artestregcod.estregdes,
    }
    print(context)
    return render(request, 'articulos/verArticulo.html', context)

def listarArticulosView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    objs = L1MArticulo.objects.all()
    context = {
        'articulos': objs,
    }
    print(context)
    return render(request, 'articulos/listarArticulo.html', context)

def crearArticulosView(request, *args, **kwargs):
    form = RawCrearArticulosForm()
    if request.method == "POST":
        form = RawCrearArticulosForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            L1MArticulo.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'articulos/crearArticulo.html', context)

def editarArticulosView(request, *args, **kwargs):
    obj = L1MArticulo.objects.get(artcod = kwargs['index'])
    initial_dict = {
        'artcodbar' : obj.artcodbar,
        'artnom': obj.artnom,
        'artdsc': obj.artdsc,
        'artpreuni': obj.artpreuni,
        'artstk': obj.artstk,
        'artestregcod': obj.artestregcod
    }
    form = RawCrearArticulosForm(request.POST or None, initial=initial_dict)
    if form.is_valid():
        L1MArticulo.objects.filter(artcod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearArticulosForm()
    else:
        print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'articulos/crearArticulo.html', context)

def eliminarArticulosView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    #articulo = L1MArticulo.objects.get(artcod = kwargs['index'])

    L1MArticulo.objects.filter(artcod = kwargs['index']).update(artestregcod=estado)
    """ setattr(articulo, "artestregcod", estado)
    articulo.save() """

    objs = L1MArticulo.objects.all()
    context = {
        'articulos': objs,
    }
    print(context)
    return render(request, 'articulos/listarArticulo.html', context)
# trabajador / listar ver crear //// admin
def trabajadorView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = R1MTrabajador.objects.get(trbcod=kwargs['index'])
    context = {
        'codigoComp': obj.trbciacod,
        'nombre': obj.trbnom,
        'con': obj.trbcon,
        'root': obj.trartt.tiposndes,
        'estado': obj.trbestreg.estregdes,
    }
    print(context)
    return render(request, 'trabajador/verTrabajador.html', context)

def listarTrabajadoresView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    objs = R1MTrabajador.objects.all()
    context = {
        'trabajadores': objs,
    }
    print(context)
    return render(request, 'trabajador/listarTrabajador.html', context)

def crearTrabajadorView(request, *args, **kwargs):
    form = RawCrearTrabajadoresForm()
    if request.method == "POST":
        form = RawCrearTrabajadoresForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            R1MTrabajador.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'trabajador/crearTrabajador.html', context)

def editarTrabajadorView(request, *args, **kwargs):
    obj = R1MTrabajador.objects.get(trbcod = kwargs['index'])
    initial_dict = {
        'trbciacod' : obj.trbciacod,
        'trbnom': obj.trbnom,
        'trbcon': obj.trbcon,
        'trartt': obj.trartt.tiposndes,
        'trbestreg': obj.trbestreg.estregdes
    }
    form = RawCrearTrabajadoresForm(request.POST or None, initial=initial_dict)
    form.fields['trartt'].initial = initial_dict['trartt']
    form.fields['trbestreg'].initial = initial_dict['trbestreg']
    if form.is_valid():
        R1MTrabajador.objects.filter(trbcod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearTrabajadoresForm()
    else:
        print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'trabajador/crearTrabajador.html', context)

def eliminarTrabajadorView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    #trabajador = R1MTrabajador.objects.get(trbcod = kwargs['index'])

    R1MTrabajador.objects.filter(trbcod = kwargs['index']).update(trbestreg=estado)
    """ setattr(trabajador, "trbestreg", estado)
    trabajador.save() """

    objs = R1MTrabajador.objects.all()
    context = {
        'trabajadores': objs,
    }
    print(context)
    return render(request, 'trabajador/listarTrabajador.html', context)
# transacciones / listar ver crear update delete
def transaccionesView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = V1TTransaccion.objects.get(tracod=kwargs['index'])
    context = {
        'codigo': obj.tracod,
        'nombre': obj.tranom,
        'desc': obj.tradsc,
        'precio': obj.trapre,
        'estado': obj.traestregcod.estregdes,
    }
    print(context)
    return render(request, 'transacciones/verTransaccion.html', context)

def listarTransaccionesView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    objs = V1TTransaccion.objects.all()
    context = {
        'transacciones': objs,
    }
    print(context)
    return render(request, 'transacciones/listarTransaccion.html', context)

def crearTransaccionesView(request, *args, **kwargs):
    form = RawCrearTransaccionesForm()
    if request.method == "POST":
        form = RawCrearTransaccionesForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            V1TTransaccion.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'transacciones/crearTransaccion.html', context)

def editarTransaccionesView(request, *args, **kwargs):
    obj = V1TTransaccion.objects.get(tracod = kwargs['index'])
    initial_dict = {
        'tranom' : obj.tranom,
        'tradsc': obj.tradsc,
        'trapre': obj.trapre,
        'traestregcod': obj.traestregcod
    }
    form = RawCrearTransaccionesForm(request.POST or None, initial=initial_dict)
    if form.is_valid():
        V1TTransaccion.objects.filter(tracod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearTransaccionesForm()
    else:
        print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'transacciones/crearTransaccion.html', context)

def eliminarTransaccionesView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    R1MTrabajador.objects.filter(tracod = kwargs['index']).update(traestreg=estado)
    """ transaccion = V1TTransaccion.objects.get(tracod = kwargs['index'])
    setattr(transaccion, "traestreg", estado)
    transaccion.save() """

    objs = V1TTransaccion.objects.all()
    context = {
        'transacciones': objs,
    }
    print(context)
    return render(request, 'transacciones/listarTransaccion.html', context)
# cliente / listar ver crear update delete
def clienteView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    obj = V2MCliente.objects.get(clicod=kwargs['index'])
    context = {
        'codigo': obj.clicod,
        'nombre': obj.clinom,
        'dni': obj.clidni,
        'estado': obj.cliestregcod.estregdes,
    }
    print(context)
    return render(request, 'cliente/verCliente.html', context)

def listarClientesView(request, *args, **kwargs):
    print(args)
    print(kwargs)
    objs = V2MCliente.objects.all()
    context = {
        'clientes': objs,
    }
    print(context)
    return render(request, 'cliente/listarCliente.html', context)

def crearClientesView(request, *args, **kwargs):
    form = RawCrearClientesForm()
    if request.method == "POST":
        form = RawCrearClientesForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            V2MCliente.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'cliente/crearCliente.html', context)

def editarClientesView(request, *args, **kwargs):
    obj = V2MCliente.objects.get(clicod = kwargs['index'])
    initial_dict = {
        'clinom' : obj.clinom,
        'clidni': obj.clidni,
        'cliestregcod': obj.cliestregcod,
    }
    form = RawCrearClientesForm(request.POST or None, initial=initial_dict)
    if form.is_valid():
        V2MCliente.objects.filter(clicod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearClientesForm()
    else:
        print(form.errors)
    context = {
        'form': form,
    }
    print(context)
    return render(request, 'cliente/crearCliente.html', context)

def eliminarClientesView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    V2MCliente.objects.filter(clicod = kwargs['index']).update(cliestregcod=estado)

    objs = V2MCliente.objects.all()
    context = {
        'clientes': objs,
    }
    print(context)
    return render(request, 'cliente/listarCliente.html', context)
