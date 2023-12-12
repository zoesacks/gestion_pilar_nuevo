from configuracion.models import Equivalencia
from .models import AsientosIngresos
from django.contrib import admin
from django.db.models import F

@admin.action(description="Buscar Clasificaciones")
def BuscarClasificaciones(modeladmin, request, queryset):
    # Filtrar solo los asientos sin clasificación
    asientos_sin_clasificacion = AsientosIngresos.objects.filter(Clasificacion__isnull=True)

    # Obtener un diccionario de equivalencias (OrigenProgramatica: Descripcion)
    equivalencias = dict(Equivalencia.objects.values_list('origen_programatica', 'descripcion'))

    # Actualizar los asientos sin clasificación
    for asiento in asientos_sin_clasificacion:
        origen_programatica = asiento.origen_programatica_agrupamiento
        if origen_programatica in equivalencias:
            descripcion = equivalencias[origen_programatica]
            asiento.clasificacion = Equivalencia.objects.filter(origen_programatica=origen_programatica).first()
            asiento.save()
