# ------------------------------------------------------------------------------------------
# Sistema de administracion - Ministerio de Desarrollo - Pilar
# Desarrollador Kevin Turkienich
# Julio 2023
# Kevin_turkienich@outlook.com
# ------------------------------------------------------------------------------------------

# Modelado de bases de datos para altas, bajas y modificaciones de datos maestros.

# ------------------------------------------------------------------------------------------
# Modulos importados
import datetime
from django.db import models
from django.forms import ValidationError
from configuracion.models import Fondo, Proveedor, Concepto, Equivalencia, Recurso, CodigoFinanciero
from django.utils import timezone
from datetime import datetime

TIPO_PRESTAMO = [ 
    ("SOLICITUD","SOLICITUD"),
    ("DEVOLUCION","DEVOLUCION")
]
MESES_CUSTOM = [ 
    ("1","ENERO"),
    ("2","FEBRERO"),
    ("3","MARZO"),
    ("4","ABRIL"),
    ("5","MAYO"),
    ("6","JUNIO"),
    ("7","JULIO"),
    ("8","AGOSTO"),
    ("9","SEPTIEMBRE"),
    ("10","OCTUBRE"),
    ("11","NOVIEMBRE"),
    ("12","DICIEMBRE")
]
EJERCICIO = [ 
    ("2020","2020"),
    ("2021","2021"),
    ("2022","2022"),
    ("2023","2023"),
    ("2024","2024"),
    ("2025","2025")
]

# ------------------------------------------------------------------------------------------
# DASHBOARD GASTOS
class AsientosGastos(models.Model):
    
    ejercicio = models.CharField(max_length=255,null=True, blank=True) 
    
    codigo = models.ForeignKey(CodigoFinanciero,on_delete=models.CASCADE,blank=True,null=True)

    jurisdiccion = models.CharField(max_length=255,null=True, blank=True) 
    jurisdiccion_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    estructura_programatica = models.CharField(max_length=255,null=True, blank=True) 
    estructura_programatica_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    fuente_financiamiento = models.CharField(max_length=255,null=True, blank=True) 
    fuente_financiamiento_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    objeto_del_gasto = models.CharField(max_length=255,null=False, blank=False) 
    objeto_del_gasto_descripcion = models.CharField(max_length=255,null=False, blank=False) 

    fecha = models.DateField(null=True, blank=True) 

    comprobante_tipo = models.CharField(max_length=255,null=False, blank=False) 
    comprobante_ejercicio = models.CharField(max_length=255,null=False, blank=False) 
    comprobante_numero = models.CharField(max_length=255,null=False, blank=False) 

    aplicacion_tipo = models.CharField(max_length=255,null=False, blank=False) 
    aplicacion_ejercicio = models.CharField(max_length=255,null=False, blank=False) 
    aplicacion_numero = models.CharField(max_length=255,null=False, blank=False) 



    oficina = models.CharField(max_length=255,null=True, blank=True) 
    oficina_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    obra = models.CharField(max_length=255,null=True, blank=True) 
    obra_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    patrimonio = models.CharField(max_length=255,null=True, blank=True) 
    patrimonio_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    proveedor_tipo = models.CharField(max_length=255,null=True, blank=True) 
    proveedor_numero = models.CharField(max_length=255,null=True, blank=True) 
    razon_social = models.CharField(max_length=255,null=True, blank=True) 

    presupuesto = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)
    preventivo = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)
    compromiso = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)
    devengado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)
    mandado_a_pagar = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)
    pagado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False,default=0)

    class Meta:
        verbose_name = 'asiento'
        verbose_name_plural ='Asientos Gastos' 
    
    def __str__(self):
        return f"Asiento #{self.pk} FF: {self.fuente_financiamiento} Comp: {self.comprobante_tipo}"


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# DASHBOARD GASTOS
class AsientosIngresos(models.Model):

    ejercicio = models.CharField(max_length=255,null=True, blank=True) 

    clasificacion = models.ForeignKey(Equivalencia,on_delete=models.CASCADE,null=True, blank=True)

    recurso_agrupamiento = models.CharField(max_length=255,null=True, blank=True) 
    recurso_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    origen_programatico_agrupamiento = models.CharField(max_length=255,null=True, blank=True) 
    origen_programatico_descripcion = models.CharField(max_length=255,null=True, blank=True) 

    fecha = models.DateField(null=False, blank=False) 

    devengado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    percibido = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)

    class Meta:
        verbose_name = 'asiento'
        verbose_name_plural ='Asientos Ingresos' 
    
    def __str__(self):
        return f"{self.clasificacion} | {self.fecha} | {self.recurso_descripcion} | ${self.percibido} |"
    
    
    def save(self, *args, **kwargs):
        self.ejercicio = str(self.fecha.year)
        super(AsientosIngresos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PRESTAMOS
class Prestamo(models.Model):
    fecha = models.DateField(null=False, blank=False) 
    gasto = models.ForeignKey(AsientosGastos,on_delete=models.PROTECT,null=True, blank=True)
    fondo = models.ForeignKey(Fondo,on_delete=models.PROTECT,null=True, blank=True)
    importe  = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    fecha_devolucion = models.DateField(null=True, blank=True) 
    pendiente = models.DecimalField(max_digits=30,decimal_places=2,default=0,blank=False,null=False)
    orden_de_pago = models.CharField(max_length=120, null=True, blank=True)
    resgistro_pagado = models.CharField(max_length=120, null=True, blank=True)
    proveedor = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        verbose_name = 'prestamo'
        verbose_name_plural ='Prestamos' 
    
    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.pendiente)
        formatted_fecha = self.fecha.strftime('%d/%m/%Y')
        if self.gasto:
            NAME = "📅 " + formatted_fecha + " | 🧾" + str(self.gasto) + " | 👤" + str(self.gasto.razon_social) + " | 💲" + formatted_importe
        else:
            NAME = "📅 " + formatted_fecha + " | 🧾 Prestamo Manual | 💲" + formatted_importe
            
        return NAME

    def clean(self):

        super().clean()

    def save(self, *args, **kwargs):
        if self.gasto:
            if self.gasto.aplicacion_tipo != 0 and self.gasto.aplicacion_tipo != "":
                self.resgistro_pagado = f'{self.gasto.aplicacion_tipo} - {self.gasto.aplicacion_ejercicio} -{self.gasto.aplicacion_ejercicio}'
                self.proveedor =  f'{self.gasto.proveedor_tipo} - {self.gasto.proveedor_numero} - {self.gasto.razon_social}'
        else:
            if self.importe > 0:
                self.pendiente = -1 * float(self.importe)
            else:
                self.pendiente = 0
        super(Prestamo, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS
class DevolucionPrestamo(models.Model):
    estado =models.BooleanField(default=0)
    fecha = models.DateField(null=False, blank=False,default=timezone.now) 
    prestamo = models.ForeignKey(Prestamo,on_delete=models.PROTECT,null=False, blank=False,limit_choices_to={'pendiente__lt': 0})
    importe  = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    fondo = models.CharField(max_length=120, null=True, blank=True)
    orden_de_pago = models.CharField(max_length=120, null=True, blank=True)
    registro_pagado = models.CharField(max_length=120, null=True, blank=True)
    proveedor = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.importe)
        NAME = str(self.fecha) + " - " + str(self.prestamo) + " - " + str(self.proveedor) + " - $" + formatted_importe
        return NAME


    def clean(self):

        if self.prestamo.pendiente == 0 or self.estado == 1:
            raise ValidationError(f"El prestamo ya está cancelado.")
        if self.prestamo.pendiente > self.importe:
            raise ValidationError(f"Está generando una devolucion por un importe superior al adeudado por el fondo. El máximo permitido es de {self.prestamo.pendiente}")
        if self.importe <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
        super().clean()

    def save(self, *args, **kwargs):


        self.fondo = self.prestamo.fondo
        self.orden_de_pago =  self.prestamo.orden_de_pago
        self.registro_pagado =  self.prestamo.resgistro_pagado
        self.proveedor =  self.prestamo.proveedor
        
        if self.prestamo.pendiente == -1 * self.importe:
            self.estado = True
        
        self.prestamo.pendiente += self.importe
        self.prestamo.save()

        super(DevolucionPrestamo, self).save(*args, **kwargs)
        
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS

class ProyeccionGastos(models.Model):
    codigo = models.CharField(max_length=120, null=True, blank=True)
    concepto = models.ForeignKey(Concepto,on_delete=models.PROTECT, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.PROTECT, null=True, blank=True)
    mes = models.CharField(max_length=255,null=False, blank=False,choices=MESES_CUSTOM) 
    ejercicio = models.CharField(max_length=255,null=False, blank=False,choices=EJERCICIO)
    periodo = models.DateField(null=True, blank=True) 
    importe = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    modificado_por  = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    fecha_modificacion = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.importe)

        if self.codigo:
            NAME = str(self.codigo) + " - " + str(self.mes) + " - " + str(self.proveedor) + " - $" + formatted_importe
        else:
            NAME = "NO SELECCIONADO - " + str(self.mes) + " - " + str(self.proveedor) + " - $" + formatted_importe

        return NAME
    
    def clean(self):

        if self.importe <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
 
        super().clean()

    def save(self, *args, **kwargs):

        mes_int = int(self.mes)
        ejercicio_int = int(self.ejercicio)
        self.periodo = datetime(ejercicio_int, mes_int, 1)

        super(ProyeccionGastos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS
class ProyeccionIngresos(models.Model):
    recurso = models.ForeignKey(Recurso,on_delete=models.PROTECT, null=True, blank=True)
    clasificacion = models.ForeignKey(Equivalencia,on_delete=models.CASCADE,null=True, blank=True)
    mes = models.CharField(max_length=255,null=False, blank=False,choices=MESES_CUSTOM) 
    ejercicio = models.CharField(max_length=255,null=False, blank=False,choices=EJERCICIO)
    periodo = models.DateField(null=True, blank=True) 
    importe = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    modificado_por  = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    fecha_modificacion = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.importe)
        NAME = str(self.recurso) + " - " + str(self.mes) + "/" + str(self.ejercicio) + " - $" + formatted_importe
        return NAME
    
    def clean(self):

        if self.importe <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
 
        super().clean()

    def save(self, *args, **kwargs):

        mes_int = int(self.mes)
        ejercicio_int = int(self.ejercicio)
        self.periodo = datetime(ejercicio_int, mes_int, 1)

        super(ProyeccionIngresos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PRESTAMOS
class Regularizacion(models.Model):
    fecha = models.DateField(null=False, blank=False) 
    gasto = models.ForeignKey(AsientosGastos,on_delete=models.PROTECT,null=False, blank=False)
    fondo = models.ForeignKey(Fondo,on_delete=models.PROTECT,null=True, blank=True)
    importe = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    registro_pagado = models.CharField(max_length=120, null=True, blank=True)
    proveedor = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Regularizacion'
        verbose_name_plural ='Regularizaciones' 
    
    def __str__(self):
        formatted_fecha = self.fecha.strftime('%d/%m/%Y')
        NAME = "📅 " + formatted_fecha + " | 🧾" + str(self.gasto) + " | 👤" + str(self.gasto.razon_social)
        return NAME

    def clean(self):

        super().clean()

    def save(self, *args, **kwargs):

        super(Regularizacion, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------