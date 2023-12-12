# Generated by Django 4.1.7 on 2023-12-12 15:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsientosGastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ejercicio', models.CharField(blank=True, max_length=255, null=True)),
                ('jurisdiccion', models.CharField(blank=True, max_length=255, null=True)),
                ('jurisdiccion_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('estructura_programatica', models.CharField(blank=True, max_length=255, null=True)),
                ('estructura_programatica_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('fuente_financiamiento', models.CharField(blank=True, max_length=255, null=True)),
                ('fuente_financiamiento_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('objeto_del_gasto', models.CharField(max_length=255)),
                ('objeto_del_gasto_descripcion', models.CharField(max_length=255)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('comprobante_tipo', models.CharField(max_length=255)),
                ('comprobante_ejercicio', models.CharField(max_length=255)),
                ('comprobante_numero', models.CharField(max_length=255)),
                ('aplicacion_tipo', models.CharField(max_length=255)),
                ('aplicacion_ejercicio', models.CharField(max_length=255)),
                ('aplicacion_numero', models.CharField(max_length=255)),
                ('oficina', models.CharField(blank=True, max_length=255, null=True)),
                ('oficina_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('obra', models.CharField(blank=True, max_length=255, null=True)),
                ('obra_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('patrimonio', models.CharField(blank=True, max_length=255, null=True)),
                ('patrimonio_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor_tipo', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor_numero', models.CharField(blank=True, max_length=255, null=True)),
                ('razon_social', models.CharField(blank=True, max_length=255, null=True)),
                ('presupuesto', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('preventivo', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('compromiso', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('devengado', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('mandado_a_pagar', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('pagado', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuracion.codigofinanciero')),
            ],
            options={
                'verbose_name': 'asiento',
                'verbose_name_plural': 'Asientos Gastos',
            },
        ),
        migrations.CreateModel(
            name='Regularizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('importe', models.DecimalField(decimal_places=2, max_digits=30)),
                ('registro_pagado', models.CharField(blank=True, max_length=120, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=120, null=True)),
                ('fondo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.fondo')),
                ('gasto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asientos.asientosgastos')),
            ],
            options={
                'verbose_name': 'Regularizacion',
                'verbose_name_plural': 'Regularizaciones',
            },
        ),
        migrations.CreateModel(
            name='ProyeccionIngresos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(choices=[('1', 'ENERO'), ('2', 'FEBRERO'), ('3', 'MARZO'), ('4', 'ABRIL'), ('5', 'MAYO'), ('6', 'JUNIO'), ('7', 'JULIO'), ('8', 'AGOSTO'), ('9', 'SEPTIEMBRE'), ('10', 'OCTUBRE'), ('11', 'NOVIEMBRE'), ('12', 'DICIEMBRE')], max_length=255)),
                ('ejercicio', models.CharField(choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], max_length=255)),
                ('periodo', models.DateField(blank=True, null=True)),
                ('importe', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('modificado_por', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('fecha_modificacion', models.CharField(blank=True, max_length=120, null=True)),
                ('clasificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuracion.equivalencia')),
                ('recurso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.recurso')),
            ],
        ),
        migrations.CreateModel(
            name='ProyeccionGastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=120, null=True)),
                ('mes', models.CharField(choices=[('1', 'ENERO'), ('2', 'FEBRERO'), ('3', 'MARZO'), ('4', 'ABRIL'), ('5', 'MAYO'), ('6', 'JUNIO'), ('7', 'JULIO'), ('8', 'AGOSTO'), ('9', 'SEPTIEMBRE'), ('10', 'OCTUBRE'), ('11', 'NOVIEMBRE'), ('12', 'DICIEMBRE')], max_length=255)),
                ('ejercicio', models.CharField(choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], max_length=255)),
                ('periodo', models.DateField(blank=True, null=True)),
                ('importe', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('modificado_por', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('fecha_modificacion', models.CharField(blank=True, max_length=120, null=True)),
                ('concepto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.concepto')),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('importe', models.DecimalField(decimal_places=2, max_digits=30)),
                ('fecha_devolucion', models.DateField(blank=True, null=True)),
                ('pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('orden_de_pago', models.CharField(blank=True, max_length=120, null=True)),
                ('resgistro_pagado', models.CharField(blank=True, max_length=120, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=120, null=True)),
                ('fondo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='configuracion.fondo')),
                ('gasto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='asientos.asientosgastos')),
            ],
            options={
                'verbose_name': 'prestamo',
                'verbose_name_plural': 'Prestamos',
            },
        ),
        migrations.CreateModel(
            name='DevolucionPrestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=0)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('importe', models.DecimalField(decimal_places=2, max_digits=30)),
                ('fondo', models.CharField(blank=True, max_length=120, null=True)),
                ('orden_de_pago', models.CharField(blank=True, max_length=120, null=True)),
                ('registro_pagado', models.CharField(blank=True, max_length=120, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=120, null=True)),
                ('prestamo', models.ForeignKey(limit_choices_to={'pendiente__lt': 0}, on_delete=django.db.models.deletion.PROTECT, to='asientos.prestamo')),
            ],
        ),
        migrations.CreateModel(
            name='AsientosIngresos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ejercicio', models.CharField(blank=True, max_length=255, null=True)),
                ('recurso_agrupamiento', models.CharField(blank=True, max_length=255, null=True)),
                ('recurso_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('origen_programatico_agrupamiento', models.CharField(blank=True, max_length=255, null=True)),
                ('origen_programatico_descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha', models.DateField()),
                ('devengado', models.DecimalField(decimal_places=2, max_digits=30)),
                ('percibido', models.DecimalField(decimal_places=2, max_digits=30)),
                ('clasificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuracion.equivalencia')),
            ],
            options={
                'verbose_name': 'asiento',
                'verbose_name_plural': 'Asientos Ingresos',
            },
        ),
    ]
