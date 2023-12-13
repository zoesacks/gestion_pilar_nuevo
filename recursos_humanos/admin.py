from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import DatosPersonales, Legajo, Sector
from .models import Cargo, Oficina

# Register your models here.

class DatosPersonalesInline(admin.StackedInline):
    model = DatosPersonales
    min_num = 1 
    max_num = 1


@admin.register(Legajo)
class LegajoAdmin(ImportExportModelAdmin):
    list_display = ('num_legajo', 'nombre', 'oficina' )
    inlines = [
        DatosPersonalesInline,
    ]

    def nombre(self, obj):
        return DatosPersonales.objects.get(legajo = obj)
    

@admin.register(Sector)
class SectorAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)


@admin.register(Cargo)
class CargoAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Oficina)
class OficinaAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)