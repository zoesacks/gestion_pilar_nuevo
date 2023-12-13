from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import FileExtensionValidator
from .legajo import Legajo
from .configuracion import *


class DatosPersonales(models.Model):
    #CAMPOS OBLIGATORIOS
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=255, choices=SEXO)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacimiento = models.DateField()
    foto = models.ImageField(
        upload_to='img/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],)
    

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    


