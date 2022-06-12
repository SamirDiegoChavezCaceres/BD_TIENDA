from django.db import models

# Create your models here.
class GzzEstadoRegistro(models.Model):
    estregcod = models.CharField(db_column='EstRegCod', primary_key=True, max_length=1)  # Field name made lowercase.
    estregdes = models.CharField(db_column='EstRegDes', max_length=40)  # Field name made lowercase.
    estregestreg = models.ForeignKey('self', models.DO_NOTHING, db_column='EstRegEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'gzz_estado_registro'


class GzzSino(models.Model):
    tiposncod = models.AutoField(db_column='TipOsnCod', primary_key=True)  # Field name made lowercase.
    tiposndes = models.CharField(db_column='TipOsnDes', max_length=40)  # Field name made lowercase.
    tiposnestreg = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='TipOsnEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'gzz_sino'


class F2MCompany(models.Model):
    ciacod = models.AutoField(db_column='CiaCod', primary_key=True)  # Field name made lowercase.
    cianom = models.CharField(db_column='CiaNom', max_length=60)  # Field name made lowercase.
    ciaruc = models.BigIntegerField(db_column='CiaRUC')  # Field name made lowercase.
    ciacap = models.DecimalField(db_column='CiaCap', max_digits=10, decimal_places=2)  # Field name made lowercase.
    ciaestregcod = models.ForeignKey('GzzEstadoRegistro', models.DO_NOTHING, db_column='CiaEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2m_compañia'


class R1MTrabajador(models.Model):
    trbcod = models.AutoField(db_column='TrbCod', primary_key=True)  # Field name made lowercase.
    trbciacod = models.ForeignKey(F2MCompany, models.DO_NOTHING, db_column='TrbCiaCod')  # Field name made lowercase.
    trbnom = models.CharField(db_column='TrbNom', max_length=60)  # Field name made lowercase.
    trbcon = models.CharField(db_column='TrbCon', max_length=10)  # Field name made lowercase.
    trartt = models.ForeignKey(GzzSino, models.DO_NOTHING, db_column='TraRtt')  # Field name made lowercase.
    trbestreg = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='TrbEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'r1m_trabajador'
        unique_together = (('trbcod', 'trbciacod'),)

        
class L1MArticulo(models.Model):
    artcod = models.AutoField(db_column='ArtCod', primary_key=True)  # Field name made lowercase.
    artcodbar = models.IntegerField(db_column='ArtCodBar')  # Field name made lowercase.
    artnom = models.CharField(db_column='ArtNom', max_length=60)  # Field name made lowercase.
    artdsc = models.CharField(db_column='ArtDsc', max_length=250)  # Field name made lowercase.
    artpreuni = models.DecimalField(db_column='ArtPreUni', max_digits=6, decimal_places=2)  # Field name made lowercase.
    artstk = models.IntegerField(db_column='ArtStk')  # Field name made lowercase.
    artestregcod = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='ArtEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'l1m_articulo'
        unique_together = (('artcod', 'artcodbar'),)


class V1TTransaccion(models.Model):
    tracod = models.AutoField(db_column='TraCod', primary_key=True)  # Field name made lowercase.
    tranom = models.CharField(db_column='TraNom', max_length=60)  # Field name made lowercase.
    tradsc = models.CharField(db_column='TraDsc', max_length=250)  # Field name made lowercase.
    trapre = models.DecimalField(db_column='TraPre', max_digits=5, decimal_places=2)  # Field name made lowercase.
    traestregcod = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='TraEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_transaccion'


class V2MCliente(models.Model):
    clicod = models.AutoField(db_column='CliCod', primary_key=True)  # Field name made lowercase.
    clinom = models.CharField(db_column='CliNom', max_length=60)  # Field name made lowercase.
    clidni = models.IntegerField(db_column='CliDNI', blank=True, null=True)  # Field name made lowercase.
    cliestregcod = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='CliEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v2m_cliente'


class V1TBoletaEleCab(models.Model):
    bolelecabcod = models.AutoField(db_column='BolEleCabCod', primary_key=True)  # Field name made lowercase.
    bolelecabfecdia = models.IntegerField(db_column='BolEleCabFecDia')  # Field name made lowercase.
    bolelecabfecmes = models.IntegerField(db_column='BolEleCabFecMes')  # Field name made lowercase.
    bolelecabfecaño = models.IntegerField(db_column='BolEleCabFecAño')  # Field name made lowercase.
    bolelecabhor = models.IntegerField(db_column='BolEleCabHor')  # Field name made lowercase.
    bolelecabmin = models.IntegerField(db_column='BolEleCabMin')  # Field name made lowercase.
    bolelecabseg = models.IntegerField(db_column='BolEleCabSeg')  # Field name made lowercase.
    bolelecabclicod = models.ForeignKey('V2MCliente', models.DO_NOTHING, db_column='BolEleCabCliCod')  # Field name made lowercase.
    bolelecabtrbcod = models.ForeignKey(R1MTrabajador, models.DO_NOTHING, db_column='BolEleCabTrbCod')  # Field name made lowercase.
    bolelecabtot = models.IntegerField(db_column='BolEleCabTot')  # Field name made lowercase.
    bolelecabestregcod = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='BolEleCabEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_cab'

        
class V1TBoletaEleDetTra(models.Model):
    boleledettrabolelecabcod = models.OneToOneField(V1TBoletaEleCab, models.DO_NOTHING, db_column='BolEleDetTraBolEleCabCod', primary_key=True)  # Field name made lowercase.
    boleledettratracod = models.ForeignKey('V1TTransaccion', models.DO_NOTHING, db_column='BolEleDetTraTraCod')  # Field name made lowercase.
    boleledettratracan = models.IntegerField(db_column='BolEleDetTraTraCan')  # Field name made lowercase.
    boleledettratraimp = models.DecimalField(db_column='BolEleDetTraTraImp', max_digits=5, decimal_places=2)  # Field name made lowercase.
    boleledettraestregcod = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='BolEleDetTraEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_det_tra'
        unique_together = (('boleledettrabolelecabcod', 'boleledettratracod'),)


class V1TBoletaEleDetArt(models.Model):
    boleledetartbolelecabcod = models.OneToOneField(V1TBoletaEleCab, models.DO_NOTHING, db_column='BolEleDetArtBolEleCabCod', primary_key=True)  # Field name made lowercase.
    boleledetartartcod = models.ForeignKey(L1MArticulo, models.DO_NOTHING, db_column='BolEleDetArtArtCod')  # Field name made lowercase.
    boleledetartartcodbar = models.ForeignKey(L1MArticulo, models.DO_NOTHING, db_column='BolEleDetArtArtCodBar')  # Field name made lowercase.
    boleledetartartcan = models.IntegerField(db_column='BolEleDetArtArtCan')  # Field name made lowercase.
    boleledetartartimp = models.DecimalField(db_column='BolEleDetArtArtImp', max_digits=5, decimal_places=2)  # Field name made lowercase.
    boleledetartestreg = models.ForeignKey(GzzEstadoRegistro, models.DO_NOTHING, db_column='BolEleDetArtEstReg')  # Field name made lowercase.

    class Meta:
        db_table = 'v1t_boleta_ele_det_art'
        unique_together = (('boleledetartbolelecabcod', 'boleledetartartcod', 'boleledetartartcodbar'),)     


class F2TPagos(models.Model):
    pagcod = models.AutoField(db_column='PagCod', primary_key=True)  # Field name made lowercase.
    pagtrbcod = models.ForeignKey('R1MTrabajador', models.DO_NOTHING, db_column='PagTrbCod')  # Field name made lowercase.
    pagnom = models.CharField(db_column='PagNom', max_length=60)  # Field name made lowercase.
    pagdsc = models.CharField(db_column='PagDsc', max_length=250)  # Field name made lowercase.
    pagpre = models.DecimalField(db_column='PagPre', max_digits=6, decimal_places=2)  # Field name made lowercase.
    pagfecaño = models.IntegerField(db_column='PagFecAño')  # Field name made lowercase.
    pagfecmes = models.IntegerField(db_column='PagFecMes')  # Field name made lowercase.
    pagfecdia = models.IntegerField(db_column='PagFecDia')  # Field name made lowercase.
    paghor = models.IntegerField(db_column='PagHor')  # Field name made lowercase.
    pagmin = models.IntegerField(db_column='PagMin')  # Field name made lowercase.
    pagseg = models.IntegerField(db_column='PagSeg')  # Field name made lowercase.
    pagestregcod = models.ForeignKey('GzzEstadoRegistro', models.DO_NOTHING, db_column='PagEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2t_pagos'


class F2HControlVen(models.Model):
    convencod = models.AutoField(db_column='ConVenCod', primary_key=True)  # Field name made lowercase.
    convenbolelecabcod = models.ForeignKey('V1TBoletaEleCab', models.DO_NOTHING, db_column='ConVenBolEleCabCod', blank=True, null=True)  # Field name made lowercase.
    convenpagcod = models.ForeignKey('F2TPagos', models.DO_NOTHING, db_column='ConVenPagCod', blank=True, null=True)  # Field name made lowercase.
    convenciacod = models.ForeignKey('F2MCompany', models.DO_NOTHING, db_column='ConVenCiaCod')  # Field name made lowercase.
    convencapfin = models.DecimalField(db_column='ConVenCapFin', max_digits=10, decimal_places=2)  # Field name made lowercase.
    convenestregcod = models.ForeignKey('GzzEstadoRegistro', models.DO_NOTHING, db_column='ConVenEstRegCod')  # Field name made lowercase.

    class Meta:
        db_table = 'f2h_control_ven'

