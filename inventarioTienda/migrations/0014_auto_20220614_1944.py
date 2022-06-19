# Generated by Django 3.2.3 on 2022-06-15 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioTienda', '0013_alter_f2tpagoscontrolven_pagconvenconvencod'),
    ]

    operations = [
        migrations.AddField(
            model_name='f2tpagoscontrolven',
            name='pagconvencod',
            field=models.AutoField(db_column='PagConVenCod', default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='f2tpagoscontrolven',
            name='pagconvenconvencod',
            field=models.ForeignKey(db_column='PagConVenConVenCod', on_delete=django.db.models.deletion.RESTRICT, to='inventarioTienda.f2hcontrolven'),
        ),
        migrations.AlterUniqueTogether(
            name='f2tpagoscontrolven',
            unique_together={('pagconvencod', 'pagconvenconvencod')},
        ),
    ]
