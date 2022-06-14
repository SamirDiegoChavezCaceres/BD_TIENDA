from datetime import date, time
from django import forms
from .models import F2HControlVen, F2MCompany, GzzEstadoRegistro

class RawControlVentasForm(forms.Form):
    convenfecaño = forms.IntegerField(initial=date.today().year, disabled=True, label="Año")
    convenfecmes = forms.IntegerField(initial=date.today().month, disabled=True, label="Mes")
    convenfecdia = forms.IntegerField(initial=date.today().day, disabled=True, label="Dia")
    convenciacod = forms.ModelChoiceField(initial=1,queryset=F2MCompany.objects.filter(ciacod=1), disabled=True, label="Compañia Codigo")
    convencapini = forms.DecimalField(initial=F2MCompany.objects.filter(ciacod=1)[0].ciacap, disabled=True, label="Capital Inicial")
    convencapfin = forms.DecimalField(initial=0, disabled=True, label="Capital Final")
    convenestregcod = forms.ModelChoiceField(initial='A',queryset=GzzEstadoRegistro.objects.filter(estregcod='A'), disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['convenfecaño'].widget.attrs.update({})
        self.fields['convenciacod'].widget.attrs.update()
        

    # def clean_contenido(self, *args, **kwargs):
    #     content = self.cleaned_data.get('contenido')
    #     if content[0].isupper():
    #         return content
    #     else:
    #         raise forms.ValidationError('La primera letra en mayuscula')
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['contenido'].widget.attrs.update({'placeholder' : 'Ingrese su pregunta aqui',
    #                                                   'class': 'preguContenido',
    #                                                   'style': "width:400px;",})

    # def clean_contenido(self, *args, **kwargs):
    #     content = self.cleaned_data.get('contenido')
    #     if content[0] == '¿' and content[-1] == '?':
    #         if len(content) >    3:
    #             return content
    #         else:
    #             raise forms.ValidationError('Minimo 3 palabras')
    #     else:
    #         raise forms.ValidationError('Debe estar entre signos de interrogacion')  