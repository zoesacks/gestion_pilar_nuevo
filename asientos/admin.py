from django import forms
from django.contrib import admin
from .models import *

import calendar
from django.db.models.functions import ExtractMonth
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db.models import Sum
from .generarPrestamo import GenerarPrestamo, GenerarRegularizacion
from .forms import ProyeccionGastosForm,ProyeccionIngresosForm
from .BuscarEquivalencias import BuscarClasificaciones

class MonthFilter(admin.SimpleListFilter):
    title = _('Mes')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = model_admin.model.objects.annotate(month=ExtractMonth('fecha')).order_by('month').values_list('month', flat=True).distinct()
        return [(month, _(calendar.month_name[month])) for month in months]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Fecha__month=self.value())

class ProveedorFilter(SimpleListFilter):
    title = _('Proveedor')
    parameter_name = 'proveedor'

    def lookups(self, request, model_admin):
        # Obtener los proveedores únicos de la base de datos
        proveedores = model_admin.get_queryset(request).values_list('ProveedorTipo', 'ProveedorNumero', 'RazonSocial').distinct()
        # Generar las opciones del filtro
        return tuple((f'{tipo} - {numero} - {razon_social}', f'{tipo} - {numero} - {razon_social}') for tipo, numero, razon_social in proveedores)

    def queryset(self, request, queryset):
        # Aplicar el filtro según la opción seleccionada
        if self.value():
            tipo, numero, razon_social = self.value().split(' - ')
            return queryset.filter(ProveedorTipo=tipo, ProveedorNumero=numero, RazonSocial=razon_social)

@admin.register(AsientosGastos)
class AsientosGastosAdmin(ImportExportModelAdmin):
    list_display=('ejercicio','fecha','Jurisdiccion','Fuente_financiamiento','Estructura_programatica','Objeto_del_gasto','Comprobante','Aplicacion','Pagado',)
    list_filter = (MonthFilter,'razon_social','aplicacion_numero','comprobante_tipo')
    ordering=('pagado',)
    list_per_page=50
    actions = [GenerarPrestamo, GenerarRegularizacion]

    def Jurisdiccion(self, obj):
        if obj.jurisdiccion:
            name = f'{obj.jurisdiccion} - {obj.jurisdiccion_descripcion}'
        else:
            name = ""
        return name 
     
    def Estructura_programatica(self, obj):
        if obj.estructura_programatica:
            name = f'{obj.estructura_programatica} - {obj.estructura_programatica_descripcion}'
        else:
            name = ""
        return name 
    
    def Fuente_financiamiento(self, obj):
        if obj.fuente_financiamiento:
            name = f'{obj.fuente_financiamiento} - {obj.fuente_financiamiento_descripcion}'
        else:
            name = ""
        return name 
    
    def Objeto_del_gasto(self, obj):
        if obj.objeto_del_gasto:
            name = f'{obj.objeto_del_gasto} - {obj.objeto_del_gasto_descripcion}'
        else:
            name = ""
        return name 
    
    def Comprobante(self, obj):
        if obj.comprobante_tipo:
            name = f'{obj.comprobante_tipo} - {obj.comprobante_ejercicio} - {obj.comprobante_numero}'
        else:
            name = ""
        return name 
    
    def Aplicacion(self, obj):
        if obj.aplicacion_tipo:
            name = f'{obj.aplicacion_tipo} - {obj.aplicacion_ejercicio} - {obj.aplicacion_numero}'
        else:
            name = ""
        return name 

    def Proveedor(self, obj):
        if obj.proveedor_tipo:
            name = f'{obj.proveedor_tipo} - {obj.proveedor_numero} - {obj.razon_social}'
        else:
            name = ""
        return name 

    def Pagado(self, obj):
        return "💲{:,.2f}".format(obj.pagado)
    
@admin.register(AsientosIngresos)
class AsientosIngresosAdmin(ImportExportModelAdmin):
    list_display=('ejercicio','fecha','clasificacion','recurso_descripcion','origen_programatico_descripcion','Devengado','Percibido',)
    list_filter = ('clasificacion','recurso_descripcion','origen_programatico_descripcion','fecha')
    ordering=('-fecha',)
    list_per_page=50
    exclude = ('ejercicio',)
    actions = [BuscarClasificaciones]

    def Devengado(self, obj):
        return "💲{:,.2f}".format(obj.devengado)
    
    def Percibido(self, obj):
        return "💲{:,.2f}".format(obj.percibido)

class PendienteZeroFilter(admin.SimpleListFilter):
    title = _('Todos los Prestamos')
    parameter_name = 'pendiente_zero'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Prestamos Cancelados')),
            ('no', _('Prestamos Pendientes')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(pendiente=0)
        if self.value() == 'no':
            return queryset.exclude(pendiente=0)

@admin.register(Prestamo)
class PrestamoAdmin(ImportExportModelAdmin):
    list_display=('gasto','fecha','fondo','Total','Pendiente_devolucion','orden_de_pago','resgistro_pagado','Proveedor','fecha_devolucion')
    exclude =('gasto',)
    list_filter = (PendienteZeroFilter,)
    
    def Total(self, obj):
        return "💲{:,.2f}".format(obj.importe)
        
    def Pendiente_devolucion(self, obj):
        return "💲{:,.2f}".format(obj.pendiente)
    
    def Proveedor(self, obj):
        MSJ = F'{obj.gasto.razon_social}'
        return MSJ
   
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        return queryset
    
    def changelist_view(self, request, extra_context=None):
        # Agregar el total al contexto de la vista
        extra_context = extra_context or {}

        # Obtener el total de los importes
        total_importes = self.get_queryset(request).aggregate(total=Sum('importe'))['total']

        # Agregar el total al contexto
        extra_context['total_importes'] = total_importes
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(DevolucionPrestamo)
class DevolucionPrestamoAdmin(ImportExportModelAdmin):
    list_display=('prestamo','fecha','Total','fondo','orden_de_pago','registro_pagado','proveedor',)
    exclude =('pendiente','fondo','orden_de_pago','registro_pagado','proveedor','estado')
    list_filter = ('prestamo',)

    def Total(self, obj):
        return "💲{:,.2f}".format(obj.importe)

class ProyeccionGastosForm(forms.ModelForm):
    class Meta:
        model = ProyeccionGastos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProyeccionGastosForm, self).__init__(*args, **kwargs)

        self.fields['proveedor'].queryset = Proveedor.objects.all()

class ProyeccionIngresosForm(forms.ModelForm):
    class Meta:
        model = ProyeccionIngresos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProyeccionIngresosForm, self).__init__(*args, **kwargs)
        # Filtrar los proveedores disponibles en el queryset del campo 'PROVEEDOR'
        self.fields['recurso'].queryset = Recurso.objects.all()

@admin.register(ProyeccionGastos)
class ProyeccionGastosAdmin(ImportExportModelAdmin):
    form = ProyeccionGastosForm
    list_display = ('codigo', 'proveedor', 'concepto', 'periodo', 'Total_proyectado','importe')
    exclude = ('modificado_por', 'fecha_modificacion', 'periodo')
    ordering = ('periodo',)
    list_editable = ('importe',)
    list_filter = ('codigo', 'proveedor', 'concepto', 'mes', 'ejercicio')

    def Total_proyectado(self, obj):
        return "💲{:,.2f}".format(obj.importe)
    
    def Periodo(self, obj):
        msj = f'{obj.mes} - {obj.ejercicio}'
        return msj

@admin.register(ProyeccionIngresos)
class ProyeccionIngresosAdmin(ImportExportModelAdmin):
    form = ProyeccionIngresosForm
    list_display = ('recurso', 'clasificacion','Periodo', 'Total_proyectado',)
    exclude = ('modificado_por', 'fecha_modificacion', 'periodo')
    ordering = ('periodo',)
    list_filter = ('recurso','mes','ejercicio')

    def Total_proyectado(self, obj):
        return "💲{:,.2f}".format(obj.importe)
    
    def Periodo(self, obj):
        msj = f'{obj.mes} - {obj.ejercicio}'
        return msj


@admin.register(Regularizacion)
class RegularizacionAdmin(ImportExportModelAdmin):
    list_display=('gasto','fecha','fondo','Total','registro_pagado','proveedor',)
    exclude =('gasto',)    
    
    def Total(self, obj):
        return "💲{:,.2f}".format(obj.importe)
