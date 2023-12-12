from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

class ComentarioInline(admin.StackedInline):
    model = SolicitudDeAyuda.comentarios.through
    extra = 1
    verbose_name = 'comentario'
    verbose_name_plural = 'Comentarios'

@admin.register(SolicitudDeAyuda)
class SolicitudDeAyudaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'usuario', 'titulo', 'fecha', 'estado')
    list_filter = ('usuario', 'estado')
    readonly_fields = ('comentarios',)
    
    inlines = [ComentarioInline]

    actions = ['comenzarSolicitudDeAyuda', 'terminarSolicitudDeAyuda']

    
    @admin.action(description="Comenzar")
    def comenzarSolicitudDeAyuda(self, obj, queryset):

        for obj in queryset:
            if obj.estado == 'Pendiente':
                obj.estado = 'En proceso'
                obj.save()

            else: 
                RuntimeError ("La solicitud debe estar pendiente")
    
    @admin.action(description="Terminar")
    def terminarSolicitudDeAyuda(self, obj, queryset):

        for obj in queryset:
            if obj.estado == 'En proceso':
                obj.estado = 'Terminado'
                obj.save()

            else: 
                RuntimeError ("La solicitud debe estar en proceso")


@admin.register(ComentarioSolicutudDeAyuda)
class ComentarioSolicutudDeAyudaAdmin(ImportExportModelAdmin):
    list_display = ('comentario',)






