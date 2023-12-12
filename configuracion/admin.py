from django.contrib import admin
from configuracion.models import *
from import_export.admin import ImportExportModelAdmin


class CodigoFinancieroFondoInline(admin.TabularInline):
    model = CodigoFinancieroFondo
    extra = 1
    fields = ('codigo', 'fondo',)

class FondoDestinoInline(admin.TabularInline):
    model = FondoDestino
    extra = 1
    fields = ('destino', 'fondo',)

class FondoRecursoInline(admin.TabularInline):
    model = FondoRecurso
    extra = 1
    fields = ('recurso', 'fondo',)

@admin.register(Concepto)
class ConceptoAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Destino)
class DestinoAdmin(ImportExportModelAdmin):
    list_display = ('agrupamiento','descripcion')
    list_filter = ('agrupamiento','descripcion')

@admin.register(Equivalencia)
class EquivalenciaAdmin(ImportExportModelAdmin):
    list_display=('origen_programatica','descripcion') 

@admin.register(Fondo)
class FondoAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'clasificacion','nombre',)
    list_filter = ('codigo',  'clasificacion','nombre',)
    inlines = [FondoDestinoInline,FondoRecursoInline]
    
@admin.register(Recurso)
class RecursoAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'nombre',)
    list_filter = ('codigo', 'nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'tipo','razon_social', 'Estado',)
    list_filter = ('codigo', 'tipo','razon_social', 'estado',)
    
    def Estado(self, obj):
        if obj.estado == 0:
            return "🔴 Inactivo"
        else:
            return "🟢 Activo"

@admin.register(CodigoFinanciero)
class CodigoFinancieroAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'descripcion','fondo_afectado')
    list_filter = ('codigo', 'fondo_afectado')
    exclude = ('fondo_afectado',)
    inlines = [CodigoFinancieroFondoInline,]



@admin.register(TipoDocumento)
class TipoDocumentoAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion','comprobante_operacion','abreviatura')
    list_filter = ('numero', 'descripcion','comprobante_operacion','abreviatura') 
    