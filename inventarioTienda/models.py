from django.db import models
from django.core.validators import (MinLengthValidator,MaxValueValidator,MinValueValidator)
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class GzzEstadoRegistro(models.Model):
    estregcod = models.CharField(db_column='EstRegCod', primary_key=True, max_length=1)  # Field name made lowercase.
    estregdes = models.CharField(db_column='EstRegDes', max_length=40)  # Field name made lowercase.
    estregestreg = models.ForeignKey('self', models.RESTRICT, db_column='EstRegEstReg', default='A')  # Field name made lowercase.

    class Meta:
        db_table = 'gzz_estado_registro'


class GzzSino(models.Model):
    tiposncod = models.AutoField(db_column='TipOsnCod', primary_key=True)  # Field name made lowercase.
    tiposndes = models.CharField(db_column='TipOsnDes', max_length=40)  # Field name made lowercase.
    tiposnestreg = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='TipOsnEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'gzz_sino'


class F2MCompany(models.Model):
    ciacod = models.AutoField(db_column='CiaCod', primary_key=True)  # Field name made lowercase.
    cianom = models.CharField(db_column='CiaNom', max_length=60)  # Field name made lowercase.
    ciaruc = models.BigIntegerField(db_column='CiaRUC', validators=[MinValueValidator(10000000000), MaxValueValidator(99999999999)])  # Field name made lowercase.
    ciacap = models.DecimalField(db_column='CiaCap', max_digits=20, decimal_places=2)  # Field name made lowercase.
    ciaestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='CiaEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2m_company'

class F2MAlmacen(models.Model):
    alncod = models.AutoField(db_column='almcod', primary_key=True)
    alndsc = models.CharField(db_column='CiaNom', max_length=360)
    alnestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='CiaEstRegCod')
    class Meta:
        db_table = 'f2m_almacen'

class R1MTrabajador(models.Model):
    trbcod = models.AutoField(db_column='TrbCod', primary_key=True)  # Field name made lowercase.
    trbciacod = models.ForeignKey(F2MCompany, models.RESTRICT, db_column='TrbCiaCod')  # Field name made lowercase.
    trbnom = models.CharField(db_column='TrbNom', max_length=60)  # Field name made lowercase.
    trbcon = models.CharField(db_column='TrbCon', max_length=10)  # Field name made lowercase.
    #trartt = models.ForeignKey(GzzSino, models.RESTRICT, db_column='TraRtt')  # Field name made lowercase.
    #https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
    trausr = models.ForeignKey(User, on_delete=models.CASCADE, db_column='TrbUsr', null=True, blank=True)
    trbestreg = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='TrbEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'r1m_trabajador'
        unique_together = (('trbcod', 'trbciacod'),)
    def get_absolute_url():
        return reverse("listarTrabajador")

class L1MArticulo(models.Model):
    artcod = models.AutoField(db_column='ArtCod', primary_key=True)  # Field name made lowercase.
    artcodbar = models.IntegerField(db_column='ArtCodBar', validators=[MaxValueValidator(9999999999999)], default=0)  # Field name made lowercase.
    artnom = models.CharField(db_column='ArtNom', max_length=60)  # Field name made lowercase.
    artdsc = models.CharField(db_column='ArtDsc', max_length=250)  # Field name made lowercase.
    artpreuni = models.DecimalField(db_column='ArtPreUni', max_digits=10, decimal_places=2)  # Field name made lowercase.
    artaln = models.ForeignKey(F2MAlmacen, models.RESTRICT, db_column='ArtAln', null=True, blank=True)
    artstk = models.IntegerField(db_column='ArtStk', validators=[MinValueValidator(0), MaxValueValidator(999)])  # Field name made lowercase.
    artestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='ArtEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'l1m_articulo'
    def get_absolute_url():
        return reverse("listarArticulo")


class V1TTransaccion(models.Model):
    tracod = models.AutoField(db_column='TraCod', primary_key=True)  # Field name made lowercase.
    tranom = models.CharField(db_column='TraNom', max_length=60)  # Field name made lowercase.
    tradsc = models.CharField(db_column='TraDsc', max_length=250)  # Field name made lowercase.
    trapre = models.DecimalField(db_column='TraPre', max_digits=10, decimal_places=2)  # Field name made lowercase.
    traestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='TraEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_transaccion'
    def get_absolute_url():
        return reverse("listarTransaccion")


class V2MCliente(models.Model):
    clicod = models.AutoField(db_column='CliCod', primary_key=True)  # Field name made lowercase.
    clinom = models.CharField(db_column='CliNom', max_length=60)  # Field name made lowercase.
    clidni = models.IntegerField(db_column='CliDNI', blank=True, null=True, validators=[MinValueValidator(10000000), MaxValueValidator(99999999)])  # Field name made lowercase.
    cliestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='CliEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v2m_cliente'
    def get_absolute_url(self):
        return reverse("verCliente", kwargs={"index": self.clicod})
  

class F2HControlVen(models.Model):
    convencod = models.AutoField(db_column='ConVenCod', primary_key=True)  # Field name made lowercase.
    #convenbolelecabcod = models.ForeignKey('V1TBoletaEleCab', models.RESTRICT, db_column='ConVenBolEleCabCod', blank=True, null=True)  # Field name made lowercase.
    #convenpagcod = models.ForeignKey(F2TPagos, models.RESTRICT, db_column='ConVenPagCod', blank=True, null=True)  # Field name made lowercase.
    convenfecaño = models.IntegerField(db_column='ConVenFecAño', validators=[MinValueValidator(2000), MaxValueValidator(2090)], null=True, blank=True)  # Field name made lowercase.
    convenfecmes = models.IntegerField(db_column='ConVenFecMes', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=True)  # Field name made lowercase.
    convenfecdia = models.IntegerField(db_column='ConVenFecDia', validators=[MinValueValidator(1), MaxValueValidator(31)], null=True, blank=True)  # Field name made lowercase.
    convenciacod = models.ForeignKey(F2MCompany, models.RESTRICT, db_column='ConVenCiaCod')  # Field name made lowercase.
    convencapini = models.DecimalField(db_column='ConVenCapIni', max_digits=20, decimal_places=2, default=0.00)  # Field name made lowercase.
    convencapfin = models.DecimalField(db_column='ConVenCapFin', max_digits=20, decimal_places=2)  # Field name made lowercase.
    convenestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='ConVenEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2h_control_ven'


class V1TBoletaEleCab(models.Model):
    bolelecabcod = models.AutoField(db_column='BolEleCabCod', primary_key=True)  # Field name made lowercase.
    bolelecabconvencod = models.ForeignKey('F2HControlVen', models.RESTRICT, null=True, blank=True, db_column='BolEleCabConVenCod')
    bolelecabfecdia = models.IntegerField(db_column='BolEleCabFecDia', validators=[MinValueValidator(1), MaxValueValidator(31)])  # Field name made lowercase.
    bolelecabfecmes = models.IntegerField(db_column='BolEleCabFecMes', validators=[MinValueValidator(1), MaxValueValidator(12)])  # Field name made lowercase.
    bolelecabfecaño = models.IntegerField(db_column='BolEleCabFecAño', validators=[MinValueValidator(2000), MaxValueValidator(2090)])  # Field name made lowercase.
    bolelecabhor = models.IntegerField(db_column='BolEleCabHor', validators=[MinValueValidator(1), MaxValueValidator(24)])  # Field name made lowercase.
    bolelecabmin = models.IntegerField(db_column='BolEleCabMin', validators=[MinValueValidator(1), MaxValueValidator(60)])  # Field name made lowercase.
    bolelecabseg = models.IntegerField(db_column='BolEleCabSeg', validators=[MinValueValidator(1), MaxValueValidator(60)])  # Field name made lowercase.
    bolelecabclicod = models.ForeignKey(V2MCliente, models.RESTRICT, db_column='BolEleCabCliCod')  # Field name made lowercase.
    bolelecabtrbcod = models.ForeignKey(R1MTrabajador, models.RESTRICT, db_column='BolEleCabTrbCod')  # Field name made lowercase.
    bolelecabtot = models.DecimalField(db_column='BolEleCabTot', max_digits=20, decimal_places=2)  # Field name made lowercase.
    bolelecabestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='BolEleCabEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_cab'
        unique_together = (('bolelecabcod', 'bolelecabconvencod'),)   
    def get_absolute_url(self):
        return reverse("boletaCabFinEst", kwargs={"index": self.bolelecabcod})
    


class F2TPagos(models.Model):
    pagcod = models.AutoField(db_column='PagCod', primary_key=True)  # Field name made lowercase.
    pagnom = models.CharField(db_column='PagNom', max_length=60)  # Field name made lowercase.
    pagdsc = models.CharField(db_column='PagDsc', max_length=250)  # Field name made lowercase.
    pagpre = models.DecimalField(db_column='PagPre', max_digits=10, decimal_places=2)  # Field name made lowercase.
    pagestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='PagEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2t_pagos' 


class F2TPagosControlVen(models.Model):
    pagconvencod = models.AutoField(db_column='PagConVenCod', primary_key=True)
    pagconvenconvencod = models.ForeignKey(F2HControlVen, models.RESTRICT, db_column='PagConVenConVenCod',)
    pagconvenpagcod = models.ForeignKey(F2TPagos, models.RESTRICT, db_column='PagConVenPagCod',null=True, blank=True, )  # Field name made lowercase.
    pagconventrbcod = models.ForeignKey(R1MTrabajador, models.RESTRICT, db_column='PagTrbCod')  # Field name made lowercase.
    pagconvenfecaño = models.IntegerField(db_column='PagFecAño', validators=[MinValueValidator(2000), MaxValueValidator(2090)])  # Field name made lowercase.
    pagconvenfecmes = models.IntegerField(db_column='PagFecMes', validators=[MinValueValidator(1), MaxValueValidator(12)])  # Field name made lowercase.
    pagconvenfecdia = models.IntegerField(db_column='PagFecDia', validators=[MinValueValidator(1), MaxValueValidator(31)])  # Field name made lowercase.
    pagconvenhor = models.IntegerField(db_column='PagHor', validators=[MinValueValidator(1), MaxValueValidator(24)] )  # Field name made lowercase.
    pagconvenmin = models.IntegerField(db_column='PagMin', validators=[MinValueValidator(1), MaxValueValidator(60)])  # Field name made lowercase.
    pagconvenseg = models.IntegerField(db_column='PagSeg', validators=[MinValueValidator(1), MaxValueValidator(60)])  # Field name made lowercase.
    pagconvenestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='PagEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2t_pagos_con_ven'
        unique_together = (('pagconvencod', 'pagconvenconvencod'),)   

class V1TBoletaEleDetTra(models.Model):
    boletadettracod = models.AutoField(db_column='BolDetTraCod', primary_key=True)
    boleledettrabolelecabcod = models.ForeignKey(V1TBoletaEleCab, models.RESTRICT, db_column='BolEleDetTraBolEleCabCod')  # Field name made lowercase.
    boleledettratracod = models.ForeignKey(V1TTransaccion, models.RESTRICT, db_column='BolEleDetTraTraCod')  # Field name made lowercase.
    boleledettratracan = models.DecimalField(db_column='BolEleDetTraTraCan', max_digits=10, decimal_places=2)  # Field name made lowercase.
    boleledettratraimp = models.DecimalField(db_column='BolEleDetTraTraImp', max_digits=10, decimal_places=2)  # Field name made lowercase.
    boleledettraestregcod = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='BolEleDetTraEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_det_tra'
        unique_together = (('boletadettracod','boleledettrabolelecabcod', 'boleledettratracod'),)


class V1TBoletaEleDetArt(models.Model):
    boleledetartcod = models.AutoField(db_column='BolDetArtCod', primary_key=True)
    boleledetartbolelecabcod = models.ForeignKey(V1TBoletaEleCab, models.RESTRICT, db_column='BolEleDetArtBolEleCabCod')  # Field name made lowercase.
    #boleledetartartcod = models.ForeignKey(L1MArticulo, models.RESTRICT, db_column='BolEleDetArtArtCod', related_name='artCod',)  # Field name made lowercase.
    boleledetartartcodbar = models.ForeignKey(L1MArticulo, models.RESTRICT, db_column='BolEleDetArtArtCodBar')  # Field name made lowercase.
    boleledetartartcan = models.DecimalField(db_column='BolEleDetArtArtCan', max_digits=10, decimal_places=2)  # Field name made lowercase.
    boleledetartartimp = models.DecimalField(db_column='BolEleDetArtArtImp', max_digits=10, decimal_places=2)  # Field name made lowercase.
    boleledetartestreg = models.ForeignKey(GzzEstadoRegistro, models.RESTRICT, db_column='BolEleDetArtEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_det_art'
        unique_together = (('boleledetartcod', 'boleledetartbolelecabcod', 'boleledetartartcodbar'),)             