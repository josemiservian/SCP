# Generated by Django 3.1.7 on 2021-04-11 22:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20210411_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2021, 4, 11, 22, 53, 43, 355668, tzinfo=utc)),
        ),
    ]
