import time
from django import forms
from .models import F2HControlVen, F2MCompany, GzzEstadoRegistro, R1MTrabajador, F2TPagos, GzzSino

class RawControlVentasForm(forms.Form):
    convenfecaño = forms.IntegerField(initial=time.localtime(time.time()).tm_year,disabled=True, label="Año")
    convenfecmes = forms.IntegerField(initial=time.localtime(time.time()).tm_mon,disabled=True, label="Mes")
    convenfecdia = forms.IntegerField(initial=time.localtime(time.time()).tm_mday,disabled=True, label="Dia")
    convenciacod = forms.ModelChoiceField(initial=1,queryset=F2MCompany.objects.filter(ciacod=1), disabled=True, label="Compañia Codigo")
    convencapini = forms.DecimalField(initial=F2MCompany.objects.filter(ciacod=1)[0].ciacap, disabled=True, label="Capital Inicial")
    convencapfin = forms.DecimalField(initial=0, disabled=True, label="Capital Final")
    convenestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")
        
class RawPagosControlVentasForm(forms.Form):
    pagconvenconvencod = forms.ModelChoiceField(queryset=F2HControlVen.objects.all(), disabled=True, label="Codigo Venta Codigo")
    pagconvenpagcod = forms.ModelChoiceField(queryset=F2TPagos.objects.all(), disabled=True, label="Codigo Pago")
    pagconventrbcod = forms.ModelChoiceField(queryset=R1MTrabajador.objects.all(), disabled=True, label="Trabajador Codigo")
    pagconvenfecaño = forms.IntegerField(initial=time.localtime(time.time()).tm_year, disabled=True, label="Año")
    pagconvenfecmes = forms.IntegerField(initial=time.localtime(time.time()).tm_mon, disabled=True, label="Mes")
    pagconvenfecdia = forms.IntegerField(initial=time.localtime(time.time()).tm_mday, disabled=True, label="Dia")
    pagconvenhor = forms.IntegerField(initial=time.localtime(time.time()).tm_hour, disabled=True, label="Hora")
    pagconvenmin = forms.IntegerField(initial=time.localtime(time.time()).tm_min, disabled=True, label="Minutos")
    pagconvenseg = forms.IntegerField(initial=time.localtime(time.time()).tm_sec, disabled=True, label="Segundos")
    pagconvenestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")

class RawPagosForm(forms.Form):
    pagnom = forms.CharField(label="Nombre")
    pagdsc = forms.CharField(label="Descripcion")
    pagpre = forms.DecimalField(label="Costo")
    pagestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")
    
class RawCrearArticulosForm(forms.Form):
    artcodbar = forms.IntegerField(label="Codigo de Barras")
    artnom = forms.CharField(label="Nombre")
    artdsc = forms.CharField(label="Descripcion")
    artpreuni = forms.DecimalField(label="Precio Unitario")
    artstk = forms.IntegerField(label="Stock")
    artestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")

class RawCrearTrabajadoresForm(forms.Form):
    trbciacod = forms.ModelChoiceField(initial=1,queryset=F2MCompany.objects.filter(ciacod=1), disabled=True, label="Compañia Codigo")
    trbnom = forms.CharField(label="Nombre")
    trbcon = forms.CharField(label="Descripcion", initial="*           ",)
    trartt = forms.ModelChoiceField(initial=1,queryset=GzzSino.objects.filter(tiposncod=2), disabled=True, label="Sesion")
    trbestreg = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")
    
class RawCrearTransaccionesForm:
    tranom = forms.CharField(label="Nombre")
    tradsc = forms.CharField(label="Descripcion")
    trapre = forms.DecimalField(label="Precio")
    traestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")

class RawCrearClientesForm:
    clinom = forms.CharField(label="Nombre")
    clidni = forms.IntegerField(label="DNI")
    cliestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True, label="Estado")
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