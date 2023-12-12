# Generated by Django 4.2.5 on 2023-12-12 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recursos_humanos', '0001_initial'),
        ('seguimiento_expedientes', '0002_remove_usuario_sector_delete_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='destinatario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destinatario', to='recursos_humanos.legajo'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propietario', to='recursos_humanos.legajo'),
        ),
        migrations.AlterField(
            model_name='transferencia',
            name='emisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to='recursos_humanos.legajo'),
        ),
        migrations.AlterField(
            model_name='transferencia',
            name='receptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to='recursos_humanos.legajo'),
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]