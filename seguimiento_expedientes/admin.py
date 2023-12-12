from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

from .models import Documento, Transferencia
from configuracion.models import TipoDocumento
from recursos_humanos.models import Legajo

class DocumentoResource(resources.ModelResource):
    tipo = fields.Field(attribute='tipo', column_name='tipo', widget=widgets.ForeignKeyWidget(TipoDocumento, 'numero')) 
    numero = fields.Field(attribute='numero', column_name='numero')
    ejercicio = fields.Field(attribute='ejercicio', column_name='ejercicio')
    propietario = fields.Field(attribute='propietario', column_name='propietario', widget=widgets.ForeignKeyWidget(Legajo, 'usuario__username'))

    class Meta:
        model = Documento
        exclude = ('fecha_alta', 'en_transito', 'destinatario', 'fecha_transito', 'observacion', 'transferencias')



@admin.register(Documento)
class DocumentoAdmin(ImportExportModelAdmin):
    resource_class = DocumentoResource
    list_display = ('tipo', 'numero', 'ejercicio', 'Propietario', 'en_transito',)
    list_filter = ('numero', 'ejercicio', 'propietario', 'en_transito',)
    readonly_fields = ('fecha_alta', 'en_transito', 'destinatario', 'fecha_transito', 'observacion', 'transferencias')

    def Propietario(self, obj):
        return obj.propietario.usuario.username
    
@admin.register(Transferencia)
class TransferenciaAdmin(ImportExportModelAdmin):
    list_display = ('fecha', 'emisor', 'receptor', 'fecha_confirmacion',)
    list_filter = ('fecha', 'emisor', 'receptor', 'fecha_confirmacion',)
    readonly_fields = ('fecha', 'emisor', 'receptor', 'fecha_confirmacion',)
    
    
