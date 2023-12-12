# ------------------------------------------------------------------------------------------
# GESTION PILAR
# Sistema de Administracion general Municipio de Pilar
# Desarrolladores:
# 
# 
# ------------------------------------------------------------------------------------------

# Modelado de bases de datos para altas, bajas y modificaciones de datos maestros.

CLASIFICACION_CODIGOS = [ 
    ("LIBRE DISPONIBILIDAD","LIBRE DISPONIBILIDAD"),
    ("AFECTADO","AFECTADO"),
]


# ------------------------------------------------------------------------------------------
# Modulos importados
from django.db import models
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PROVEEDOR
class Proveedor(models.Model):
    estado = models.BooleanField(default=0)
    codigo = models.CharField(max_length=50,null=False, blank=False)
    tipo = models.CharField(max_length=50,null=True, blank=True)
    razon_social = models.CharField(max_length=255, null=True, blank=True)
    domicilio = models.CharField(max_length=255, null=True, blank=True) 
    fecha_inscripcion = models.DateField(null=True, blank=True)
    cuit = models.CharField(max_length=255, null=True, blank=True)
    ramo = models.CharField(max_length=255, null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)

    

    def __str__(self):
        NAME = str(self.codigo) + " - " + str(self.tipo) + " - " + str(self.razon_social)
        return NAME
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 


# ------------------------------------------------------------------------------------------  
# ------------------------------------------------------------------------------------------
# CLASE RECURSO
class Recurso(models.Model):
    codigo = models.CharField(verbose_name='Agrupamiento',max_length=50,unique=True,null=False, blank=False)
    nombre = models.CharField(verbose_name='Descripcion',max_length=2550, null=True, blank=False)


    def __str__(self):
        NAME = f'{self.codigo} - {self.nombre}'
        return NAME
    
    class Meta:
        verbose_name = 'recurso'
        verbose_name_plural ='Recursos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DESTINO
class Destino(models.Model):
    agrupamiento = models.CharField(max_length=50,unique=True,null=True, blank=True)
    descripcion = models.TextField()


    def __str__(self):
        NAME = f'{self.agrupamiento} - {self.descripcion}'
        return NAME
    
    class Meta:
        verbose_name = 'destino'
        verbose_name_plural ='Destinos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class Fondo(models.Model):
    codigo = models.CharField(max_length=20,unique=True,null=False, blank=False)
    clasificacion = models.CharField(max_length=20, choices=CLASIFICACION_CODIGOS,default="LIBRE DISPONIBILIDAD",null=True, blank=True)
    nombre = models.CharField(max_length=120, null=False, blank=False)
    total = models.DecimalField(max_digits=30, decimal_places=2,default=0)

    def __str__(self):
        NAME = str(self.codigo) + " - " + str(self.nombre)
        return NAME
    
    class Meta:
        verbose_name = 'fondo'
        verbose_name_plural ='Fondos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class Concepto(models.Model):
    nombre = models.CharField(max_length=120, null=False, blank=False,unique=True)

    def __str__(self):
        NAME = str(self.nombre)
        return NAME
    
    class Meta:
        verbose_name = 'concepto'
        verbose_name_plural ='Conceptos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE EQUIVALENCAIS
class Equivalencia(models.Model):
    origen_programatica = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'equivalencia'
        verbose_name_plural ='Equivalencias' 

    def __str__(self):
        return f"{self.origen_programatica} | {self.descripcion}"
    

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO FINANCIERO
class CodigoFinanciero(models.Model):
    codigo = models.CharField(max_length=20,unique=True,null=False, blank=False)
    descripcion = models.CharField(max_length=150,null=True, blank=True)
    fondo_afectado = models.ForeignKey(Fondo, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        NAME = str(self.codigo)
        return NAME
    
    class Meta:
        verbose_name = 'codigo'
        verbose_name_plural ='Codigos financieros' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO-FONDO
class CodigoFinancieroFondo(models.Model):
    codigo = models.ForeignKey(CodigoFinanciero,on_delete=models.CASCADE,null=False, blank=False)
    fondo = models.ForeignKey(Fondo,on_delete=models.CASCADE,null=False, blank=False)

    def __str__(self):
        NAME = str(self.codigo) + " - " + str(self.fondo)
        return NAME
    
    class Meta:
        verbose_name = 'fondo'
        verbose_name_plural ='Asignacion de Fondos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO-FONDO
class FondoRecurso(models.Model):
    fondo = models.ForeignKey(Fondo,on_delete=models.CASCADE,null=True, blank=True)
    recurso = models.ForeignKey(Recurso,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        NAME = str(self.fondo) + " - " + str(self.recurso)
        return NAME
    
    class Meta:
        verbose_name = 'recurso'
        verbose_name_plural ='Asignacion de Recursos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO-FONDO
class FondoDestino(models.Model):
    fondo = models.ForeignKey(Fondo,on_delete=models.CASCADE,null=True, blank=True)
    destino = models.ForeignKey(Destino,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        NAME = str(self.fondo) + " - " + str(self.destino)
        return NAME
    
    class Meta:
        verbose_name = 'destino'
        verbose_name_plural ='Asignacion de Destinos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE TIPO DOCUMENTOS
class TipoDocumento(models.Model):
    numero = models.IntegerField(unique=True,blank=False,null=False)
    descripcion = models.CharField(max_length = 255,blank=True,null=True)
    comprobante_operacion = models.CharField(max_length = 255,blank=True,null=True)
    abreviatura = models.CharField(max_length = 10,blank=True,null=True)

    def __str__(self):
        return f'{self.numero}'
    
    class Meta:
        verbose_name = 'tipo de documento'
        verbose_name_plural ='Tipos de documentos'