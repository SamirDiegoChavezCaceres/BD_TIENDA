# Generated by Django 3.2.3 on 2023-02-01 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioTienda', '0027_auto_20230131_2005'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='r1mtrabajador',
            unique_together={('trbcod', 'trbciacod')},
        ),
    ]