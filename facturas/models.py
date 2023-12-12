from django.db import models

from configuracion.models import CodigoFinanciero


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FACTURA
# class Factura(models.Model):

#     emision = models.DateField(blank=True, null = True)
#     alta = models.DateField(blank=True, null = True)
#     tipo_factura = models.CharField(max_length = 255, blank=True, null = True)
#     nro_factura = models.CharField(max_length = 255, blank=True, null = True)
#     proveedor = models.CharField(max_length = 255, blank=True, null = True)
#     total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null = True)
#     codigo = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=True, null = True)

#     #CAMPOS NO OBLIGATORIOS

#     oc = models.CharField(max_length = 255, blank=True, null = True)
#     ff = models.CharField(max_length = 255, blank=True, null = True)
#     unidad_ejecutora = models.CharField(max_length = 255, blank=True, null = True)
#     objeto = models.CharField(max_length = 255, blank=True, null = True)
#     fondo_afectado = models.CharField(max_length = 255, blank=True, null = True)
#     ubicacion = models.CharField(max_length = 255, blank=True, null = True)

#     #CAMPOS PARA MANEJO DE AUTORIZACION
#     devengado = models.BooleanField(default=False)
#     autorizado = models.BooleanField(default=False)
#     autorizado_por = models.CharField(max_length=255, blank=True, null=True)
#     autorizado_fecha = models.DateTimeField(blank=True, null=True)