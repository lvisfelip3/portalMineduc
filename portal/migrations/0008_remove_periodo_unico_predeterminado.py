# Generated by Django 5.0.4 on 2024-06-15 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_remove_periodo_unico_predeterminado_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='periodo',
            name='unico_predeterminado',
        ),
    ]
