# Generated by Django 3.1.6 on 2021-06-01 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregable',
            name='responsable',
        ),
    ]
