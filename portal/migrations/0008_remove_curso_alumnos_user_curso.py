# Generated by Django 5.0.4 on 2024-06-12 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_curso_alumnos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='alumnos',
        ),
        migrations.AddField(
            model_name='user',
            name='curso',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='portal.curso'),
        ),
    ]
