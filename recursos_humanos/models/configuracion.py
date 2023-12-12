from django.db import models
from django.core.validators import MinValueValidator

SEXO = [
    ("F", "femenino"), 
    ("M", "masculino"),
]

class Oficina(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Cargo(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)


class Sector(models.Model):
    nombre = models.CharField(max_length = 255, unique=True)

    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = 'sector'
        verbose_name_plural ='Sectores'

    def clean(self):   
        super().clean() 