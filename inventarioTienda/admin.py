from django.contrib import admin

# Register your models here.
from .models import GzzEstadoRegistro
from .models import GzzSino
from .models import F2MCompany
from .models import R1MTrabajador
from .models import L1MArticulo
from .models import V1TTransaccion
from .models import V2MCliente
from .models import V1TBoletaEleCab
from .models import V1TBoletaEleDetTra
from .models import V1TBoletaEleDetArt
from .models import F2TPagos
from .models import F2HControlVen
from .models import F2TPagosControlVen
from .models import F2MAlmacen

admin.site.register(GzzEstadoRegistro)
admin.site.register(GzzSino)
admin.site.register(F2MCompany)
admin.site.register(R1MTrabajador)
admin.site.register(L1MArticulo)
admin.site.register(V1TTransaccion)
admin.site.register(V2MCliente)
admin.site.register(V1TBoletaEleCab)
admin.site.register(V1TBoletaEleDetTra)
admin.site.register(V1TBoletaEleDetArt)
admin.site.register(F2TPagos)
admin.site.register(F2HControlVen)
admin.site.register(F2TPagosControlVen)
admin.site.register(F2MAlmacen)
