# Generated by Django 5.0.4 on 2024-06-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_remove_curso_alumnos_user_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='edad',
            field=models.IntegerField(default=''),
        ),
    ]
