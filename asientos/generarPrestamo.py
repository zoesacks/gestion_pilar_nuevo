
from datetime import date
from django.contrib import admin
from django.contrib import messages
from .models import Prestamo, Regularizacion

@admin.action(description="Generar Prestamo")
def GenerarPrestamo(modeladmin, request, queryset):
    if queryset.count() == 1:
        obj = queryset.first()
        if obj.fuente_financiamiento != "1.1.0 - TESORO MUNICIPAL":
            if obj.pagado > 0:
                nuevo_prestamo = Prestamo(
                    fecha=date.today(),
                    gasto=obj,
                    importe=obj.ppagado,
                    pendiente=-obj.pagado,
                    registro_pagado=f'{obj.aplicacion_tipo} - {obj.aplicacion_ejercicio} - {obj.aplicacion_numero}',
                    proveedor=f'{obj.proveedor_tipo} - {obj.proveedor_numero} - {obj.razon_social}'
                )
                nuevo_prestamo.save()
            else:
                messages.warning(request, "El importe Pagado es menor o igual a $ 0.-")
        
        else:
            messages.warning(request, "La fuente de financiamiento del gasto seleccionado no corresponde a '1.1.0 - Tesoro municipal', por favor seleccione otro gasto.")
    else:
        messages.warning(request, "Solo se puede generar un prestamo a la vez. Por favor seleccione 1 solo registro.")





@admin.action(description="Generar Regularizacion")
def GenerarRegularizacion(modeladmin, request, queryset):
    
    if queryset.count() == 1:

        obj = queryset.first()

        if obj.fuente_financiamiento == "1.1.0":
            if obj.pagado < 0:
                nueva_regularizacion = Regularizacion(
                    fecha=date.today(),
                    gasto=obj,
                    importe=obj.pagado,
                    registro_pagado=f'{obj.aplicacion_tipo} - {obj.aplicacion_ejercicio} - {obj.aplicacion_numero}',
                    proveedor=f'{obj.proveedor_tipo} - {obj.proveedor_numero} - {obj.razon_social}'
                )
                nueva_regularizacion.save()
            else:
                messages.warning(request, "El importe Pagado es mayor o igual a $ 0.- las regularizaciones de los gastos deben ser negativas.")
        
        else:
            messages.warning(request, "La fuente de financiamiento del gasto seleccionado no corresponde a '1.1.0 - Tesoro municipal', por favor seleccione otro gasto.")
    else:
        messages.warning(request, "Solo se puede generar una regularizacion a la vez. Por favor seleccione 1 solo registro del pagado.")