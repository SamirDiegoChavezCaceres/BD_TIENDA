# Generated by Django 3.2.3 on 2022-06-17 06:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioTienda', '0014_auto_20220614_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l1marticulo',
            name='artcodbar',
            field=models.IntegerField(db_column='ArtCodBar', validators=[django.core.validators.MinValueValidator(1000000000000), django.core.validators.MaxValueValidator(9999999999999)]),
        ),
    ]
