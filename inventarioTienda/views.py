from decimal import Decimal
from django.shortcuts import render, redirect
from .models import *;
from .forms import *;
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
import logging
loggerDjango = logging.getLogger('django')
loggerRequest = logging.getLogger('django.request')
loggerInventario = logging.getLogger('DBTienda')
loggerMenu = logging.getLogger('menuAndWelcome')
#https://stackoverflow.com/questions/3209906/django-return-redirect-with-parameters
#https://mattsegal.dev/file-logging-django.html
#logger.info('The info message')
#logger.warning('The warning message')
#logger.error('The error message')
CANTIDAD_PERMITIDA = 3
# Create your views here.
# control ventas / listar ver crear

def controlVentasCapital(**kwargs):
    control = F2HControlVen.objects.get(convencod=kwargs['index'])
    montoAntiguo = kwargs['montoAntiguo']
    montoNuevo = kwargs['montoNuevo']
    balance = montoNuevo - montoAntiguo

    controlcapfin = control.convencapfin + balance

    F2HControlVen.objects.filter(convencod=kwargs['index']).update(convencapfin=controlcapfin)
    F2MCompany.objects.filter(ciacod=control.convenciacod.ciacod).update(ciacap=controlcapfin)
    

def impresionView(request, *args, **kwargs):
    ##print(args)
    #print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
    }
    ##print(context)
    loggerRequest.info(f'{request.user.username} abre la pestaña para imprimir la boleta {boletaCab.bolelecabcod} del Control {boletaCab.bolelecabconvencod.convencod} para el cliente {boletaCab.bolelecabclicod.clinom}')
    return render(request, 'imprimir/tabla.html', context)

def controlVentasView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    
    control = F2HControlVen.objects.get(convencod=kwargs['index'])
    boletas = V1TBoletaEleCab.objects.filter(bolelecabconvencod=kwargs['index'])
    pagos = F2TPagosControlVen.objects.filter(pagconvenconvencod=kwargs['index'])
    context = {
        'control': control,
        'boletas': boletas,
        'pagos': pagos,
    }
    ##print(context)
    loggerRequest.info(f'{request.user.username} consulto el Control de Ventas {kwargs["index"]}')
    return render(request, 'controlVentas/verControlVentas.html', context)

def listarControlVentasView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    controles = F2HControlVen.objects.all()
    context = {
        'controles': controles,
    }
    loggerRequest.info(f'{request.user.username} listo los Controles de Ventas')
    return render(request, 'controlVentas/listarControlVentas.html', context)

def crearControlVentasView(request):
    form = RawControlVentasForm()
    if request.method == "POST":
        form = RawControlVentasForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            F2HControlVen.objects.create(**form.cleaned_data)
            loggerInventario.info(f'{request.user.username} creo con exito el control de ventas del dia')
        else:
            loggerInventario.warning(f'{request.user.username} error en creacion de control de ventas {form.errors}')
            #print(form.errors)
    context = {
        'form': form,
    }
    
    return render(request, 'controlVentas/crearControlVentas.html', context)

# compania / ver 
def companyView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    obj = F2MCompany.objects.get(ciacod=kwargs['index'])
    context = {
        'codigo': obj.ciacod,
        'nombre': obj.cianom,
        'ruc': obj.ciaruc,
        'capital': obj.ciacap,
        'estado': obj.ciaestregcod.estregdes,
    }
    ##print(context)
    loggerRequest.info(f'{request.user.username} consulto compañia')
    return render(request, 'company/verCompany.html', context)

"""#logger.info('The info message')
#logger.warning('The warning message')
#logger.error('The error message')

loggerDjango = logging.getLogger('django')
loggerRequest = logging.getLogger('django.request')
loggerInventario = logging.getLogger('inventarioTienda')
loggerMenu = menuandwelcome"""

# pagosConVen / ver crear 
def pagoControlVentasView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
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
    ##print(context)
    return render(request, 'pagos/verPagosControlVentas.html', context)

def crearPagoControlVentasView(request): 
    
    comp = F2MCompany.objects.get(ciacod=1) 
    estado = GzzEstadoRegistro.objects.get(estregcod='A')

    controlven, created = F2HControlVen.objects.get_or_create(
        convenfecaño=time.localtime(time.time()).tm_year,
        convenfecmes=time.localtime(time.time()).tm_mon,
        convenfecdia=time.localtime(time.time()).tm_mday,
        defaults={'convenciacod': comp, 'convencapini': comp.ciacap, 'convencapfin': comp.ciacap, 'convenestregcod': estado},
    )
    if(created):
        #print("Created!")
        loggerInventario.info(f'{request.user.username} creo con exito el control de ventas del dia')

    #trabajador = R1MTrabajador.objects.get(trartt=1)
    trabajador = R1MTrabajador.objects.get(trausr=request.user)
    index = request.POST.get('indexPago')
    pago = F2TPagos.objects.get(pagcod=index) 

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
            #print(form.cleaned_data)
            pagoControl = F2TPagosControlVen.objects.create(**form.cleaned_data)

            control = F2HControlVen.objects.get(convencod=pagoControl.pagconvenconvencod.convencod)
            controlCapAnt = controlven.convencapfin
            controlCapNuevo = controlCapAnt - pagoControl.pagconvenpagcod.pagpre

            F2HControlVen.objects.filter(convencod=pagoControl.pagconvenconvencod.convencod).update(convencapfin=controlCapNuevo)
            F2MCompany.objects.filter(ciacod=control.convenciacod.ciacod).update(ciacap=controlCapNuevo)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    rendered = render_to_string('pagos/crearPagosControlVentas.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    loggerRequest.debug(f'envia la vista de crear pago control ventas al usuario {request.user.username}')
    ##print(response)
    return response

# pagos / listar ver crear update delete
def pagosView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    pago = F2TPagos.objects.get(pagcod=kwargs['index'])
    context = {
        'codigo': pago.pagcod,
        'nombre': pago.pagnom,
        'descripcion': pago.pagdsc,
        'precio': pago.pagpre,
        'estado': pago.pagestregcod,
    }
    loggerRequest.debug(f'envia la vista de pagos al usuario {request.user.username}')
    ##print(context)
    return render(request, 'pagos/verPago.html', context)

def listarPagosView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    pagos = F2TPagos.objects.all()
    context = {
        'pagos': pagos,
    }
    loggerRequest.debug(f'envia la vista de listar pagos al usuario {request.user.username}')
    return render(request, 'pagos/listarPagos.html', context)

def crearPagosView(request):
    form = RawPagosForm()
    if request.method == "POST":
        form = RawPagosForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            F2TPagos.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form,
    }
    loggerRequest.debug(f'envia la vista de crear pagos al usuario {request.user.username}')
    return render(request, 'pagos/crearPagos.html', context)
# boleta cab / ver crear 
def boletaCabeceraFinalView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=kwargs['index'])
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=kwargs['index'])
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
    }
    ##print(context)
    loggerRequest.debug(f'envia la vista de boleta cabecera final editable al usuario {request.user.username}')
    return render(request, 'boleta/verBoletaCabFin.html', context)
    
def boletaCabeceraFinalEstView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=kwargs['index'])
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=kwargs['index'])
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    ##print(context)
    loggerRequest.debug(f'envia la vista de boleta cabecera final estatico al usuario {request.user.username}')
    return render(request, 'boleta/crearBoletaCab.html', context)

def crearBoletaCabeceraView(request, *args, **kwargs):
    comp = F2MCompany.objects.get(ciacod=1)
    estado = GzzEstadoRegistro.objects.get(estregcod='A')

    controlven, created = F2HControlVen.objects.get_or_create(
        convenfecaño=time.localtime(time.time()).tm_year,
        convenfecmes=time.localtime(time.time()).tm_mon,
        convenfecdia=time.localtime(time.time()).tm_mday,
        defaults={'convenciacod': comp, 'convencapini': comp.ciacap, 'convencapfin': comp.ciacap, 'convenestregcod': estado},
    )
    if(created):
        loggerInventario.info(f'{request.user.username} crea el control de ventas {controlven}')
    #trabajador = R1MTrabajador.objects.get(trartt=1)
    trabajador = R1MTrabajador.objects.get(trausr=request.user)
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
    if(created):
        loggerInventario.info(f'{request.user.username} crea el cliente')
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
    ##print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    ##print(response)
    loggerRequest.debug(f'envia la vista de boleta cabecera editable al usuario {request.user.username}')
    return response

def deleteBoletaCabView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')

    bolArticulos = V1TBoletaEleDetArt.objects.filter(
        boleledetartbolelecabcod=kwargs['index'], 
        boleledetartestreg=estado,
        )
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(
        boleledettrabolelecabcod=kwargs['index'],
        boleledettraestregcod=estado,
        )
    importeAntiguo = 0
    importeNuevo = 0
    #print(bolArticulos)
    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    
    for articulo in bolArticulos.iterator():
        importeAntiguo =+ Decimal(articulo.boleledetartartimp)
    bolArticulos.update(boleledetartestreg=estado)
    
    for transaccion in bolTransacciones.iterator():
        importeAntiguo =+ Decimal(transaccion.boleledettratraimp)
    bolTransacciones.update(boleledettraestregcod=estado)

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

    loggerInventario.debug(f'{request.user.username} elimina los elementos de la boleta {boletaCab.bolelecabcod}')

    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo) 

    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
                                                                    bolelecabtot=(totalNuevo),
                                                                    bolelecabestregcod = estado,
                                                                    )
    loggerInventario.info(f'{request.user.username} elimina la boleta {boletaCab.bolelecabcod}')
    """  setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
    dict = {
        'index': boletaCab.bolelecabconvencod.convencod,
        'montoAntiguo': totalAntiguo,
        'montoNuevo': totalNuevo,
    }
    controlVentasCapital(**dict)
    ##print(context)
    succes_url=V1TBoletaEleCab.get_absolute_url(boletaCab)
    return redirect(succes_url)

# boleta det / crear update delete
def crearBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    if (V1TTransaccion.objects.filter(tracod=kwargs['indexTra']).exists() and kwargs['indexTra'] != ""):
        boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
            boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
            boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
            boleledettraestregcod=estado,
            defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00,},
        )
        if(created):
            loggerInventario.debug(f'{request.user.username} agrega la transaccion {boletaDet.boleledettratracod.tracod} a la boleta {boletaDet.boleledettrabolelecabcod.bolelecabcod}')

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

        boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
        bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
        bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

        context = {
            'boletaCab': boletaCab,
            'bolArticulos': bolArticulos,
            'bolTransacciones': bolTransacciones,
            'edit': True,
        }
        ##print(context
        rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
        ##print(rendered)
        response = JsonResponse(rendered, safe=False)
        ##print(response)
        return response
    else:
        loggerInventario.warning(f'{request.user.username} intenta agregar una transaccion que no existe')
        messages.info(request, 'No existe dicha transaccion')

    response = JsonResponse(data=1, status=400, safe = False)
    loggerRequest.debug(f'enviando respuesta {response}')
    return response
    

def updateBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
        boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
        boleledettraestregcod=estado,
        defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00,},
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
    
    loggerInventario.info(f'{request.user.username} actualiza la transaccion {boletaDet.boleledettratracod.tracod} de la boleta {boletaCab.bolelecabcod} de {importeAntiguo} a {importeNuevo} y el total de la boleta de {totalAntiguo} a {totalNuevo}')

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
    ##print(context)
    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    ##print(response)
    loggerRequest.debug(f'enviando vista de actualizacion')
    return response
    

def deleteBoletaDetTraView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetTra.objects.get_or_create(
        boleledettrabolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledettratracod=V1TTransaccion.objects.get(tracod=kwargs['indexTra']),
        boleledettraestregcod=estado,
        defaults={'boleledettratracan': 0.00, 'boleledettratraimp': 0.00,},
    )
    importeAntiguo = Decimal(boletaDet.boleledettratraimp)
    importeNuevo = 0
    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    V1TBoletaEleDetTra.objects.filter(boletadettracod=boletaDet.boletadettracod).update(
                                                                    boleledettraestregcod=estado,
                                                                    )
    loggerInventario.info(f'{request.user.username} elimina la transaccion {boletaDet.boleledettratracod.tracod} de la boleta {boletaDet.boleledettrabolelecabcod.bolelecabcod} ')
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
    loggerInventario.debug(f'{request.user.username} actualiza la transaccion {boletaDet.boleledettratracod.tracod} de la boleta {boletaCab.bolelecabcod} de {importeAntiguo} a {importeNuevo} y el total de la boleta de {totalAntiguo} a {totalNuevo}')
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
    ##print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    ##print(response)
    loggerRequest.debug(f'enviando vista de eliminacion')
    return response
#//////////////////////////
def crearBoletaDetArtView(request, *args, **kwargs):
    if ((L1MArticulo.objects.filter(artcod=kwargs['indexArt']).exists() or 
                L1MArticulo.objects.filter(artcodbar=kwargs['indexArt']).exists()) and kwargs['indexArt'] != ""):
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
        loggerInventario.info(f'{request.user.username} crea el articulo {boletaDet.boleledetartartcodbar.artcod} de la boleta {boletaDet.boleledetartbolelecabcod.bolelecabcod} ')
        stockPosible = L1MArticulo.objects.get(artcodbar=kwargs['indexArt']).artstk-1
        if(stockPosible >= 0):
            producto = L1MArticulo.objects.get(artcod=boletaDet.boleledetartartcodbar.artcod)    

            importeAntiguo = Decimal(boletaDet.boleledetartartimp)
            importeNuevo = Decimal(boletaDet.boleledetartartimp)+producto.artpreuni

            V1TBoletaEleDetArt.objects.filter(boleledetartcod=boletaDet.boleledetartcod).update(
                boleledetartartcan=(boletaDet.boleledetartartcan+1),
                boleledetartartimp=(importeNuevo),
            )

            L1MArticulo.objects.filter(artcod=boletaDet.boleledetartartcodbar.artcod).update(
                artstk=(stockPosible)
                )

            if(stockPosible <= CANTIDAD_PERMITIDA):
                messages.info(request, 'Stock bajo: Considere reponer.')
            """ setattr(boletaDet, "boleledetartartcan", (boletaDet.boleledetartartcan+1))
            setattr(boletaDet, "boleledetartartimp", (importeNuevo))
            setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-1))
            boletaDet.save()
            boletaDet.boleledetartartcodbar.save() """

            boletaCab = boletaDet.boleledetartbolelecabcod
            
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
            
            boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index'])
            bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
            bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)

            context = {
                'boletaCab': boletaCab,
                'bolArticulos': bolArticulos,
                'bolTransacciones': bolTransacciones,
                'edit': True,
            }
            ##print(context)

            rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
            ##print(rendered)
            response = JsonResponse(rendered, safe=False)
            ##print(response)
            return response
        else:
            messages.info(request, 'La cantidad actual no cubre la demanda actual.')
            loggerInventario.warning(f'{request.user.username} no puede agregar el articulo {boletaDet.boleledetartartcodbar.artcod} de la boleta {boletaDet.boleledetartbolelecabcod.bolelecabcod} por falta de stock')
    else:
        messages.info(request, 'No existe tal articulo')
        loggerInventario.warning(f'{request.user.username} no puede agregar el articulo {kwargs["indexArt"]} de la boleta {kwargs["index"]} por falta de articulo')
    response = JsonResponse(data=1, status=400, safe = False)
    return response
    
    

def updateBoletaDetArtView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcod=kwargs['indexArt']),
        boleledetartestreg=estado,
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00,},
    )
    
    cantidadAnt = boletaDet.boleledetartartcan
    cantidadNue = kwargs['cantidad']
    balance = cantidadNue-cantidadAnt
    #print(boletaDet.boleledetartartcodbar.artstk)
    #print(balance)
    stockPosible = boletaDet.boleledetartartcodbar.artstk-balance
    if(stockPosible >= 0):
        importeAntiguo = Decimal(boletaDet.boleledetartartimp)
        importeNuevo = Decimal(cantidadNue*boletaDet.boleledetartartcodbar.artpreuni)


        V1TBoletaEleDetArt.objects.filter(boleledetartcod=boletaDet.boleledetartcod).update(
            boleledetartartcan=(cantidadNue),
            boleledetartartimp=(importeNuevo),
            )
        L1MArticulo.objects.filter(artcod=boletaDet.boleledetartartcodbar.artcod).update(
            artstk= (boletaDet.boleledetartartcodbar.artstk-(balance))
            )
        
        """ setattr(boletaDet, "boleledetartartcan", (cantidadNue))
        setattr(boletaDet, "boleledetartartimp", (importeNuevo))
        setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt)))
        boletaDet.save()
        boletaDet.boleledetartartcodbar.save() """

        boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
        
        totalAntiguo = Decimal(boletaCab.bolelecabtot)
        totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)

        V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
            bolelecabtot=(totalNuevo),
            )
        loggerInventario.info(f'{request.user.username} actualizo el articulo {boletaDet.boleledetartartcodbar.artcod} de la boleta {boletaDet.boleledetartbolelecabcod.bolelecabcod} de {cantidadAnt} a {cantidadNue} y de {importeAntiguo} a {importeNuevo} y de {totalAntiguo} a {totalNuevo} y de {boletaDet.boleledetartartcodbar.artstk} a {stockPosible}')
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
    else:
        messages.info(request, 'El stock actual no cubre la demanda actual.')
        loggerInventario.warning(f'{request.user.username} no puede actualizar por falta de stock')

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
    
    context = {
        'boletaCab': boletaCab,
        'bolArticulos': bolArticulos,
        'bolTransacciones': bolTransacciones,
        'edit': True,
    }
    ##print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    ##print(response)
    loggerRequest.debug(f'enviando vista de editar boleta {boletaCab.bolelecabcod}')
    return response

def deleteBoletaDetArtView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='A')
    boletaDet, created = V1TBoletaEleDetArt.objects.get_or_create(
        boleledetartbolelecabcod=V1TBoletaEleCab.objects.get(bolelecabcod=kwargs['index']),
        boleledetartartcodbar=L1MArticulo.objects.get(artcod=kwargs['indexArt']),
        boleledetartestreg=estado,
        defaults={'boleledetartartcan': 0.00, 'boleledetartartimp': 0.00,},
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
    loggerInventario.info(f'{request.user.username} elimino el articulo {boletaDet.boleledetartartcodbar.artcod} de la boleta {boletaDet.boleledetartbolelecabcod.bolelecabcod}')
    """ setattr(boletaDet, "boleledettraestregcod", estado)
    setattr(boletaDet.boleledetartartcodbar, "artstk", (boletaDet.boleledetartartcodbar.artstk-(cantidadNue-cantidadAnt)))
    boletaDet.save()
    boletaDet.boleledetartartcodbar.save() """

    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    bolArticulos = V1TBoletaEleDetArt.objects.filter(boleledetartbolelecabcod=boletaCab.bolelecabcod)
    bolTransacciones = V1TBoletaEleDetTra.objects.filter(boleledettrabolelecabcod=boletaCab.bolelecabcod)
    
    totalAntiguo = Decimal(boletaCab.bolelecabtot)
    totalNuevo = totalAntiguo + (importeNuevo - importeAntiguo)
    ##print(totalNuevo)
    V1TBoletaEleCab.objects.filter(bolelecabcod=boletaCab.bolelecabcod).update(
        bolelecabtot=(totalNuevo),
        )
    loggerInventario.info(f'{request.user.username} actualizo el total de la boleta {boletaCab.bolelecabcod} de {totalAntiguo} a {totalNuevo}')
    """ setattr(boletaCab, "bolelecabtot", (totalNuevo))
    boletaCab.save() """
    boletaCab = V1TBoletaEleCab.objects.get(bolelecabcod=boletaDet.boleledetartbolelecabcod.bolelecabcod)
    #print(totalAntiguo)
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
    ##print(context)

    rendered = render_to_string('boleta/crearBoletaCabEdit.html', context)
    ##print(rendered)
    response = JsonResponse(rendered, safe=False)
    ##print(response)
    loggerRequest.debug(f'enviando vista de elminar articulo {boletaCab.bolelecabcod}')
    return response
# articulos / listar ver crear update delete
def articulosView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    obj = L1MArticulo.objects.get(artcod=kwargs['index'])
    context = {
        'codigo': obj.artcodbar,
        'nombre': obj.artnom,
        'desc': obj.artdsc,
        'precio': obj.artpreuni,
        'artaln': obj.artaln,
        'stock': obj.artstk,
        'estado': obj.artestregcod.estregdes,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista ver articulo {obj.artcod}')
    return render(request, 'articulos/verArticulo.html', context)

def listarArticulosView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    objs = L1MArticulo.objects.all()
    context = {
        'articulos': objs,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista listar articulos')
    return render(request, 'articulos/listarArticulo.html', context)

def crearArticulosView(request, *args, **kwargs):
    form = RawCrearArticulosForm()
    if request.method == "POST":
        form = RawCrearArticulosForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            L1MArticulo.objects.create(**form.cleaned_data)
            loggerInventario.info(f'{request.user.username} creo el articulo {form.cleaned_data["artcodbar"]}')
        else:
            #print(form.errors)
            loggerInventario.warning(f'{request.user.username} intento crear el articulo {form.cleaned_data["artcodbar"]} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista crear articulo')
    return render(request, 'articulos/crearArticulo.html', context)

def editarArticulosView(request, *args, **kwargs):
    obj = L1MArticulo.objects.get(artcod = kwargs['index'])
    initial_dict = {
        'artcodbar' : obj.artcodbar,
        'artnom': obj.artnom,
        'artdsc': obj.artdsc,
        'artaln': obj.artaln,
        'artpreuni': obj.artpreuni,
        'artstk': obj.artstk,
        'artestregcod': obj.artestregcod
    }
    form = RawCrearArticulosForm(request.POST or None, initial=initial_dict)
    if form.is_valid():
        L1MArticulo.objects.filter(artcod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearArticulosForm()
        loggerInventario.info(f'{request.user.username} edito el articulo {obj.artcodbar}')
    else:
        #print(form.errors)
        loggerInventario.warning(f'{request.user.username} intento editar el articulo {obj.artcodbar} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    return render(request, 'articulos/crearArticulo.html', context)

def eliminarArticulosView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    #articulo = L1MArticulo.objects.get(artcod = kwargs['index'])

    L1MArticulo.objects.filter(artcod = kwargs['index']).update(artestregcod=estado)
    """ setattr(articulo, "artestregcod", estado)
    articulo.save() """
    success_url = L1MArticulo.get_absolute_url()
    loggerInventario.info(f'{request.user.username} elimino el articulo {kwargs["index"]}')
    ##print(context)
    return redirect(success_url)

# trabajador / listar ver crear //// admin
def trabajadorView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    obj = R1MTrabajador.objects.get(trbcod=kwargs['index'])
    context = {
        'codigoComp': obj.trbciacod,
        'nombre': obj.trbnom,
        'con': obj.trbcon,
        'user': obj.trausr.username,
        'estado': obj.trbestreg.estregdes,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista ver trabajador {obj.trbcod}')
    return render(request, 'trabajador/verTrabajador.html', context)

def listarTrabajadoresView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    objs = R1MTrabajador.objects.all()
    context = {
        'trabajadores': objs,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista listar trabajadores')
    return render(request, 'trabajador/listarTrabajador.html', context)

def crearTrabajadorView(request, *args, **kwargs):
    form = RawCrearTrabajadoresForm()
    if request.method == "POST":
        form = RawCrearTrabajadoresForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            R1MTrabajador.objects.create(**form.cleaned_data)
            loggerInventario.info(f'{request.user.username} creo el trabajador {form.cleaned_data["trbciacod"]}')
        else:
            #print(form.errors)
            loggerInventario.warning(f'{request.user.username} intento crear el trabajador {form.cleaned_data["trbciacod"]} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista crear trabajador')
    return render(request, 'trabajador/crearTrabajador.html', context)

def editarTrabajadorView(request, *args, **kwargs):
    obj = R1MTrabajador.objects.get(trbcod = kwargs['index'])
    initial_dict = {
        'trbciacod' : obj.trbciacod,
        'trbnom': obj.trbnom,
        'trbcon': obj.trbcon,
        'trausr': obj.trausr,
        'trbestreg': obj.trbestreg
    }
    form = RawCrearTrabajadoresForm(request.POST or None, initial=initial_dict)
    form.fields['trausr'].initial = initial_dict['trausr']
    form.fields['trbestreg'].initial = initial_dict['trbestreg']
    if form.is_valid():
        R1MTrabajador.objects.filter(trbcod = kwargs['index']).update(**form.cleaned_data)
        form = RawCrearTrabajadoresForm()
        loggerInventario.info(f'{request.user.username} edito el trabajador {obj.trbciacod}')
    else:
        #print(form.errors)
        loggerInventario.warning(f'{request.user.username} intento editar el trabajador {obj.trbciacod} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista editar trabajador')
    return render(request, 'trabajador/crearTrabajador.html', context)

def eliminarTrabajadorView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    #trabajador = R1MTrabajador.objects.get(trbcod = kwargs['index'])

    R1MTrabajador.objects.filter(trbcod = kwargs['index']).update(trbestreg=estado)
    """ setattr(trabajador, "trbestreg", estado)
    trabajador.save() """

    ##print(context)
    success_url = R1MTrabajador.get_absolute_url()
    loggerInventario.info(f'{request.user.username} elimino el trabajador {kwargs["index"]}')
    ##print(context)
    loggerRequest.debug(f'enviando vista eliminar trabajador')
    return redirect(success_url)

# transacciones / listar ver crear update delete
def transaccionesView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    obj = V1TTransaccion.objects.get(tracod=kwargs['index'])
    context = {
        'codigo': obj.tracod,
        'nombre': obj.tranom,
        'desc': obj.tradsc,
        'precio': obj.trapre,
        'estado': obj.traestregcod.estregdes,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista ver transaccion {obj.tracod}')
    return render(request, 'transacciones/verTransaccion.html', context)

def listarTransaccionesView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    objs = V1TTransaccion.objects.all()
    context = {
        'transacciones': objs,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista listar transacciones')
    return render(request, 'transacciones/listarTransaccion.html', context)

def crearTransaccionesView(request, *args, **kwargs):
    form = RawCrearTransaccionesForm()
    if request.method == "POST":
        form = RawCrearTransaccionesForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            V1TTransaccion.objects.create(**form.cleaned_data)
            loggerInventario.info(f'{request.user.username} creo la transaccion {form.cleaned_data["tranom"]}')
        else:
            #print(form.errors)
            loggerInventario.warning(f'{request.user.username} intento crear la transaccion {form.cleaned_data["tranom"]} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista crear transaccion')
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
        loggerInventario.info(f'{request.user.username} edito la transaccion {obj.tranom}')
    else:
        #print(form.errors)
        loggerInventario.warning(f'{request.user.username} intento editar la transaccion {obj.tranom} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista editar transaccion {obj.tracod}')
    return render(request, 'transacciones/crearTransaccion.html', context)

def eliminarTransaccionesView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')

    V1TTransaccion.objects.filter(tracod = kwargs['index']).update(traestregcod=estado)
    """ transaccion = V1TTransaccion.objects.get(tracod = kwargs['index'])
    setattr(transaccion, "traestreg", estado)
    transaccion.save() """

    success_url = V1TTransaccion.get_absolute_url()
    loggerInventario.info(f'{request.user.username} elimino la transaccion {kwargs["index"]}')
    ##print(context)
    loggerRequest.debug(f'enviando vista eliminar transaccion {kwargs["index"]}')
    return redirect(success_url)

# cliente / listar ver crear update delete
def clienteView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    obj = V2MCliente.objects.get(clicod=kwargs['index'])
    boletas = V1TBoletaEleCab.objects.filter(bolelecabclicod=obj)
    context = {
        'codigo': obj.clicod,
        'nombre': obj.clinom,
        'dni': obj.clidni,
        'estado': obj.cliestregcod.estregdes,
        'boletas': boletas,
    }
    ##print(context)
    loggerRequest.info(f'enviando vista ver cliente {obj.clicod}')
    return render(request, 'cliente/verCliente.html', context)

def listarClientesView(request, *args, **kwargs):
    #print(args)
    #print(kwargs)
    objs = V2MCliente.objects.all()
    context = {
        'clientes': objs,
    }
    ##print(context)
    loggerRequest.info(f'enviando vista listar clientes')
    return render(request, 'cliente/listarCliente.html', context)

def crearClientesView(request, *args, **kwargs):
    form = RawCrearClientesForm()
    if request.method == "POST":
        form = RawCrearClientesForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            V2MCliente.objects.create(**form.cleaned_data)
            loggerInventario.info(f'{request.user.username} creo el cliente {form.cleaned_data["clinom"]}')
        else:
            #print(form.errors)
            loggerInventario.warning(f'{request.user.username} intento crear el cliente {form.cleaned_data["clinom"]} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista crear cliente')
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
        loggerInventario.info(f'{request.user.username} edito el cliente {obj.clinom}')
    else:
        #print(form.errors)
        loggerInventario.warning(f'{request.user.username} intento editar el cliente {obj.clinom} pero hubo un error')
    context = {
        'form': form,
    }
    ##print(context)
    loggerRequest.debug(f'enviando vista editar cliente {obj.clicod}')
    return render(request, 'cliente/crearCliente.html', context)

def eliminarClientesView(request, *args, **kwargs):
    estado = GzzEstadoRegistro.objects.get(estregcod='I')
    V2MCliente.objects.filter(clicod = kwargs['index']).update(cliestregcod=estado)

    success_url = V2MCliente.get_absolute_url()
    ##print(context)
    loggerRequest.debug(f'enviando vista eliminar cliente {kwargs["index"]}')
    return redirect(success_url)
