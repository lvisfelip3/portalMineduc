# Generated by Django 5.0.6 on 2024-06-15 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_alter_curso_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='predeterminado',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
