import time
from django import forms
from .models import F2HControlVen, F2MCompany, GzzEstadoRegistro, R1MTrabajador, F2TPagos, GzzSino, F2MAlmacen
from django.forms import ModelChoiceField
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class AlmacenChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.alndsc

class CompanyChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.cianom

class EstadoRegistroChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.estregdes

class ControlVenChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.convencod} - {obj.convenfecdia}/{obj.convenfecmes}/{obj.convenfecaño}'

class PagosChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.pagnom

class TrabajadorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.trbnom

class SinoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.tiposndes

class UserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.username

@sync_to_async
class RawControlVentasForm(forms.Form):
    convenfecaño = forms.IntegerField(
        initial=time.localtime(time.time()).tm_year,
        disabled=True,
        label="Año"
    )
    convenfecmes = forms.IntegerField(initial=time.localtime(time.time()).tm_mon,disabled=True, label="Mes")
    convenfecdia = forms.IntegerField(initial=time.localtime(time.time()).tm_mday,disabled=True, label="Dia")
    convenciacod = CompanyChoiceField(initial=1,queryset=F2MCompany.objects.filter(ciacod=1), disabled=True, label="Compañia Codigo")
    convencapini = forms.DecimalField(initial=F2MCompany.objects.filter(ciacod=1)[0].ciacap, disabled=True, label="Capital Inicial")
    convencapfin = forms.DecimalField(initial=0, disabled=True, label="Capital Final")
    convenestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")
        
@sync_to_async
class RawPagosControlVentasForm(forms.Form):
    pagconvenconvencod = ControlVenChoiceField(queryset=F2HControlVen.objects.all(), disabled=True, label="Codigo Venta Codigo")
    pagconvenpagcod = PagosChoiceField(queryset=F2TPagos.objects.all(), disabled=True, label="Codigo Pago")
    pagconventrbcod = TrabajadorChoiceField(queryset=R1MTrabajador.objects.all(), disabled=True, label="Trabajador Codigo")
    pagconvenfecaño = forms.IntegerField(initial=time.localtime(time.time()).tm_year, disabled=True, label="Año")
    pagconvenfecmes = forms.IntegerField(initial=time.localtime(time.time()).tm_mon, disabled=True, label="Mes")
    pagconvenfecdia = forms.IntegerField(initial=time.localtime(time.time()).tm_mday, disabled=True, label="Dia")
    pagconvenhor = forms.IntegerField(initial=time.localtime(time.time()).tm_hour, disabled=True, label="Hora")
    pagconvenmin = forms.IntegerField(initial=time.localtime(time.time()).tm_min, disabled=True, label="Minutos")
    pagconvenseg = forms.IntegerField(initial=time.localtime(time.time()).tm_sec, disabled=True, label="Segundos")
    pagconvenestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")

@sync_to_async
class RawPagosForm(forms.Form):
    pagnom = forms.CharField(label="Nombre")
    pagdsc = forms.CharField(label="Descripcion")
    pagpre = forms.DecimalField(label="Costo")
    pagestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")

@sync_to_async
class RawCrearArticulosForm(forms.Form):
    artcodbar = forms.IntegerField(label="Codigo de Barras", required=False, initial=0)
    artnom = forms.CharField(label="Nombre")
    artdsc = forms.CharField(label="Descripcion")
    artpreuni = forms.DecimalField(label="Precio Unitario")
    artaln = AlmacenChoiceField(initial=1,queryset=F2MAlmacen.objects.all(), label="Lugar")
    artstk = forms.IntegerField(label="Stock")
    artestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")

@sync_to_async
class RawCrearTrabajadoresForm(forms.Form):
    trbciacod = CompanyChoiceField(initial=1,queryset=F2MCompany.objects.filter(ciacod=1), disabled=True, label="Compañia Codigo")
    trbnom = forms.CharField(label="Nombre")
    trbcon = forms.CharField(label="Descripcion", initial="*           ",)
    trausr = UserChoiceField(initial=1,queryset=User.objects.all(), disabled=False, label="Usuario")
    trbestreg = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")

@sync_to_async
class RawCrearTransaccionesForm(forms.Form):
    tranom = forms.CharField(label="Nombre")
    tradsc = forms.CharField(label="Descripcion")
    trapre = forms.DecimalField(label="Precio")
    traestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")

@sync_to_async
class RawCrearClientesForm:
    clinom = forms.CharField(label="Nombre")
    clidni = forms.IntegerField(label="DNI")
    cliestregcod = EstadoRegistroChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.all(), disabled=False, label="Estado")
    # def clean_contenido(self, *args, **kwargs):
    #     content = self.cleaned_data.get('contenido')
    #     if content[0].isupper():
    #         return content
    #     else:
    #         raise forms.ValidationError('La primera letra en mayuscula')

    # def clean_contenido(self, *args, **kwargs):
    #     content = self.cleaned_data.get('contenido')
    #     if content[0] == '¿' and content[-1] == '?':
    #         if len(content) >    3:
    #             return content
    #         else:
    #             raise forms.ValidationError('Minimo 3 palabras')
    #     else:
    #         raise forms.ValidationError('Debe estar entre signos de interrogacion')  