"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from menuAndWelcome.views import inicioView, licenciaView
from inventarioTienda.views import (controlVentasView, listarControlVentasView, crearControlVentasView,
                                    companyView, pagoControlVentasView, crearPagoControlVentasView,
                                    pagosView, listarPagosView, crearPagosView, boletaCabeceraFinalView,
                                    crearBoletaCabeceraView, crearBoletaDetTraView, updateBoletaDetTraView,
                                    deleteBoletaDetTraView, crearBoletaDetArtView, updateBoletaDetArtView,
                                    deleteBoletaDetArtView, boletaCabeceraFinalEstView, articulosView,
                                    listarArticulosView, crearArticulosView, editarArticulosView, eliminarArticulosView,
                                    trabajadorView, listarTrabajadoresView, crearTrabajadorView, editarTrabajadorView,
                                    eliminarTrabajadorView, transaccionesView, listarTransaccionesView, crearTransaccionesView,
                                    editarTransaccionesView, eliminarTransaccionesView, clienteView, listarClientesView,
                                    crearClientesView, editarClientesView, eliminarClientesView, impresionView)

urlpatterns = [
    path('', inicioView, name="inicio"),
    path('licencia/', licenciaView, name="licencia"),

    path('controlVentas/<int:index>', controlVentasView, name="controlVentas"),
    path('listarControlVentas/', listarControlVentasView, name="listarControlVentas"),
    path('crearControlVentas/', crearControlVentasView, name="crearControlVentas"),

    path('company/<int:index>', companyView, name="company"),

    path('pagoControl/<int:index>', pagoControlVentasView, name="pagoControlVentas"),
    path('crearPagoControl/', crearPagoControlVentasView, name="crearPagoControlVentas"),

    path('pagos/<int:index>', pagosView, name="pagos"),
    path('listarPagos/', listarPagosView, name="listarPagos"),
    path('crearPagos/', crearPagosView, name="crearPagos"),

    path('boletaCabFin/<int:index>', boletaCabeceraFinalView, name="boletaCabFin"),
    path('crearBoletaCab/<nombre>/<int:dni>', crearBoletaCabeceraView, name="crearBoletaCabFin"),
    path('boletaCabFinEst/<int:index>', boletaCabeceraFinalEstView, name="boletaCabFinEst"),

    path('crearBoletaDetTra/<int:index>/<int:indexTra>', crearBoletaDetTraView, name="crearBoletaDetTra"),
    path('updateBoletaDetTra/<int:index>/<int:indexTra>/<int:cantidad>', updateBoletaDetTraView, name="updateBoletaDetTra"),
    path('deleteBoletaDetTra/<int:index>/<int:indexTra>', deleteBoletaDetTraView, name="deleteBoletaDetTra"),
    
    path('crearBoletaDetArt/<int:index>/<int:indexArt>', crearBoletaDetArtView, name="crearBoletaDetArt"),
    path('updateBoletaDetArt/<int:index>/<int:indexArt>/<int:cantidad>', updateBoletaDetArtView, name="updateBoletaDetArt"),
    path('deleteBoletaDetArt/<int:index>/<int:indexArt>', deleteBoletaDetArtView, name="deleteBoletaDetArt"),

    path('articulos/<int:index>', articulosView, name="verArticulos"),
    path('listarArticulo/', listarArticulosView, name="listarArticulo"),
    path('crearArticulo/', crearArticulosView, name="crearArticulo"),
    path('editarArticulo/<int:index>', editarArticulosView, name="editarArticulo"),
    path('eliminarArticulo/<int:index>', eliminarArticulosView, name="eliminarArticulo"),

    path('trabajadores/<int:index>', trabajadorView, name="verTrabajador"),
    path('listarTrabajador/', listarTrabajadoresView, name="listarTrabajador"),
    path('crearTrabajador/', crearTrabajadorView, name="crearTrabajador"),
    path('editarTrabajador/<int:index>', editarTrabajadorView, name="editarTrabajador"),
    path('eliminarTrabajador/<int:index>', eliminarTrabajadorView, name="eliminarTrabajador"),

    path('transacciones/<int:index>', transaccionesView, name="verTransaccion"),
    path('listarTransaccion/', listarTransaccionesView, name="listarTransaccion"),
    path('crearTransaccion/', crearTransaccionesView, name="crearTransaccion"),
    path('editarTransaccion/<int:index>', editarTransaccionesView, name="editarTransaccion"),
    path('eliminarTransaccion/<int:index>', eliminarTransaccionesView, name="eliminarTransaccion"),

    path('clientes/<int:index>', clienteView, name="verCliente"),
    path('listarCliente/', listarClientesView, name="listarCliente"),
    path('crearCliente/', crearClientesView, name="crearCliente"),
    path('editarCliente/<int:index>', editarClientesView, name="editarCliente"),
    path('eliminarCliente/<int:index>', eliminarClientesView, name="eliminarCliente"),

    path('imprimir/<int:index>', impresionView, name="eliminarCliente"),

    path('admin/', admin.site.urls),
]
