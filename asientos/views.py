from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AsientosGastos,ProyeccionGastos
import datetime
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage

@login_required(login_url='/admin/login/')
def ingresos(request):

    user_name = request.user.username
    puesto = 'Coordinador'

    context = {
        'titulo' : '',
        'user' : user_name,
        'puesto':puesto,
        }

    return render(request, 'ingresos.html', context)


@login_required(login_url='/admin/login/')
def prestamos(request):

    user_name = request.user.username
    puesto = 'Coordinador'

    context = {
        'titulo' : '',
        'user' : user_name,
        'puesto':puesto,
        }

    return render(request, 'prestamos.html', context)





@login_required(login_url='/admin/login/')
def gastos(request):

    # datos de usuario
    user_name = request.user.username
    puesto = 'Puesto'


# ---------------------------------------------------------------------------------------------------------------   
    # Inicializacion de variables

    total_gastos=0
    total_gastos_af=0
    total_gastos_ld=0

# ---------------------------------------------------------------------------------------------------------------  
    # Datos estaticos
    fecha_actual = datetime.datetime.now()

    gastos_queryset = AsientosGastos.objects.all()
    proyecciones_queryset = ProyeccionGastos.objects.all()    

     # Filtra los gastos por FuenteFinanciamiento
    gastos_ld_queryset = gastos_queryset.filter(fuente_financiamiento="1.1.0")
    gastos_af_queryset = gastos_queryset.exclude(fuente_financiamiento="1.1.0")


# ---------------------------------------------------------------------------------------------------------------   
    # CALCULO DE TOTALES PARA TARJETAS SUPERIORES

    # Calcula el total de pagados por libre disponibilidad
    total_gastos_ld = gastos_ld_queryset.aggregate(total_pagado=Sum('pagado'))['total_pagado'] or 0
    total_gastos_ld_millones = total_gastos_ld / 1000000 if total_gastos_ld > 1000000 else total_gastos_ld
    
    # Calcula el total de pagados por afectados
    total_gastos_af = gastos_af_queryset.aggregate(total_pagado=Sum('pagado'))['total_pagado'] or 0
    total_gastos_af_millones = total_gastos_af / 1000000 if total_gastos_af > 1000000 else total_gastos_af

    # Calcula el total de pagados general
    total_gastos = gastos_queryset.aggregate(total_pagado=Sum('pagado'))['total_pagado'] or 0
    total_gastos_millones = total_gastos / 1000000 if total_gastos > 1000000 else total_gastos

    # Calcula el total proyectado de gastos
    total_proyeccion = proyecciones_queryset.aggregate(total_proyectado=Sum('importe'))['total_proyectado'] or 0
    total_proyeccion_millones = total_proyeccion / 1000000 if total_proyeccion > 1000000 else total_proyeccion


# ---------------------------------------------------------------------------------------------------------------   
    # CALCULO DE TOTALES PARA TARJETAS SUPERIORES






# ---------------------------------------------------------------------------------------------------------------   
    # Configuración de paginación
    items_per_page = 20  # Número de elementos por página

    paginator = Paginator(gastos_queryset, items_per_page)
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    if not page_number:
        page_number = 1
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Mostrar la última página si está vacía


    context = {
        'titulo' : '',
        'user' : user_name,
        'puesto':puesto,

        'total_gastos':total_gastos_millones,
        'total_proyeccion':total_proyeccion_millones,
        'total_gastos_ld':total_gastos_ld_millones,
        'total_gastos_af':total_gastos_af_millones,

        'page_obj':page_obj,
        }

    return render(request, 'gastos.html', context)








# @login_required(login_url='/admin/login/')
# def gastos(request):

#     fecha_actual = datetime.datetime.now()
#     mes_actual = meses[fecha_actual.month - 1]

#     # ------ Calculo de gastos pagados -------
#     gastos_Pagado = asientosGastos.objects.filter(Fecha__month=fecha_actual.month).aggregate(total_pagados=Sum('Pagado'))
#     total_mes = gastos_Pagado['total_pagados'] if gastos_Pagado['total_pagados'] is not None else 0
    
#     # Filtrar proveedores distintos
#     proveedores = asientosGastos.objects.values_list('RazonSocial', flat=True).distinct()

#     # Filtrar codigos distintos
#     codigos = proyeccionGastos.objects.values_list('CODIGO', flat=True).distinct()

#     # Obtener los parámetros de los filtros (si están presentes)
#     fecha_desde = request.GET.get('fecha_desde')
#     fecha_hasta = request.GET.get('fecha_hasta')
#     proveedores_seleccionados = request.GET.getlist('proveedor')
#     codigos_seleccionados = request.GET.getlist('codigo')

#     # Obtener todos los objetos asientosGastos
#     gastos_query = asientosGastos.objects.all().filter(Fecha__year=2023).order_by('Fecha') #FuenteFinanciamiento="1.1.0", 

#     proyecciones = proyeccionGastos.objects.all()

#     # Aplicar los filtros si están presentes
#     if fecha_desde and fecha_hasta:
#         # Convertir las fechas de texto a objetos datetime
#         fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
#         fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
#         # Filtrar por rango de fechas
#         gastos_query = gastos_query.filter(Fecha__range=(fecha_desde, fecha_hasta))
#         proyecciones = proyecciones.filter(PERIODO__range=(fecha_desde, fecha_hasta))

#     if proveedores_seleccionados:
#         # Filtrar por proveedores seleccionados
#         gastos_query = gastos_query.filter(RazonSocial__in=proveedores_seleccionados)
#         proyecciones = proyecciones.filter(PROVEEDOR__RAZON_SOCIAL__in=proveedores_seleccionados)

#     if codigos_seleccionados:
#         gastos_query = gastos_query.filter(Codigo__CODIGO__in=codigos_seleccionados)
#         proyecciones = proyecciones.filter(CODIGO__in=codigos_seleccionados)
    
# # ------ Calculo de gastos pagados  ------- 


#     # calculo del total para tarjetas
#     total_pagado = gastos_query.aggregate(total_pagado=Sum('Pagado')/1000000)

#     gastos_mes_pagado = {}
#     for gasto in gastos_query:
#         mes = gasto.Fecha.month
#         total = gasto.Pagado
#         gastos_mes_pagado[mes] = gastos_mes_pagado.get(mes, 0) + total
        

#     Pagados_lista = []
#     for mes in range(1, 13):
#         total_mes = gastos_mes_pagado.get(mes, 0)
#         Pagados_lista.append({'mes': meses[mes - 1], 'total': total_mes})

#     gastos_mes_pagado_ld = {}
#     gastos_mes_pagado_af = {}
#     for gasto in gastos_query:
#         mes = gasto.Fecha.month
#         total = gasto.Pagado
        
#         if gasto.FuenteFinanciamiento == "1.1.0":
#             gastos_mes_pagado_ld[mes] = gastos_mes_pagado_ld.get(mes, 0) + total

#         else:
#             gastos_mes_pagado_af[mes] = gastos_mes_pagado_af.get(mes, 0) + total


#     Pagados_lista_ld = []
#     total_ld = 0
#     for mes in range(1, 13):
#         total_mes = gastos_mes_pagado_ld.get(mes, 0)
#         total_ld = total_ld + total_mes
#         Pagados_lista_ld.append({'mes': meses[mes - 1], 'total': total_mes})

#     Pagados_lista_af = []
#     total_af = 0
#     for mes in range(1, 13):
#         total_mes = gastos_mes_pagado_af.get(mes, 0)
#         total_af = total_af + total_mes
#         Pagados_lista_af.append({'mes': meses[mes - 1], 'total': total_mes})


# # ------ Calculo de gastos proyectados  ------- 

#     # calculo del total para tarjetas
#     total_proyecciones = 0

#     proyectado_mes_pagado = {}
#     for x in proyecciones:
#         mes = x.MES
#         total = x.IMPORTE
#         proyectado_mes_pagado[mes] = proyectado_mes_pagado.get(mes, 0) + total
#         total_proyecciones += total

#     Proyectado_lista = []
#     for mes in range(1, 13):
#         total_mes = proyectado_mes_pagado.get(str(mes), 0)
#         if total_mes != 0:
#             Proyectado_lista.append({'mes': meses[mes - 1], 'total': total_mes})
#         else:
#             Proyectado_lista.append({'mes': meses[mes - 1], 'total': 0})

#     total_proyecciones = total_proyecciones / 1000000

#     # calculo del desvio
#     if total_pagado['total_pagado']:
#         if total_proyecciones > total_pagado['total_pagado']:

#             desvio = round((total_proyecciones / total_pagado['total_pagado']) * 100,2)
#         else:
#             if total_proyecciones <= 0:
#                 desvio = -100
#             else:
#                 desvio = round((total_proyecciones / total_pagado['total_pagado']) * -100,2)
#     else:
#         desvio = 0

#     # Configuración de paginación

#     items_per_page = 200  # Número de elementos por página

#     paginator = Paginator(gastos_query, items_per_page)
#     page_number = request.GET.get('page')  # Obtener el número de página de la URL
#     if not page_number:
#         page_number = 1
#     try:
#         page_obj = paginator.page(page_number)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)  # Mostrar la última página si está vacía

#     if total_ld > 1000000:
#         total_ld = total_ld / 1000000

#     if total_af > 1000000:
#         total_af = total_af / 1000000

#     context = {
#         'user' : 'Turkienich',
#         'titulo' : 'Asientos Gastos',
#         'desvio':desvio,
#         'mes_actual' : mes_actual,
#         'total_mes' : total_mes,
#         'total_pagado':total_pagado,
#         'proveedores':proveedores,
#         'codigos' : codigos,
#         'Pagados_lista' : Pagados_lista,
#         'Proyectado_lista':Proyectado_lista,
#         'proyecciones':proyecciones,
#         'total_proyecciones':total_proyecciones,
#         'page_obj': page_obj,
#         'Pagados_lista_ld':Pagados_lista_ld,
#         'Pagados_lista_af':Pagados_lista_af,
#         'total_ld':total_ld,
#         'total_af':total_af,
#         }
    
#     return render(request, 'gastos.html', context)

