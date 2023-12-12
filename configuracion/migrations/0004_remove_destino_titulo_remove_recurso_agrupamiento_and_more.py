# Generated by Django 4.1.7 on 2023-12-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0003_recurso_agrupamiento_alter_recurso_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destino',
            name='titulo',
        ),
        migrations.RemoveField(
            model_name='recurso',
            name='agrupamiento',
        ),
        migrations.AddField(
            model_name='destino',
            name='agrupamiento',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
