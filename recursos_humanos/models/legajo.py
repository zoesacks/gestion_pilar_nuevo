from django.db import models
from django.contrib.auth.models import User
from .configuracion import *


class Legajo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    num_legajo = models.IntegerField(unique=True)
    oficina = models.ForeignKey(Oficina, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    superior_inmediato = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='legajos_subalternos')
    
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        from .datosPersonales import DatosPersonales
        nombre = DatosPersonales.objects.get(legajo__id = self.id).nombre
        apellido = DatosPersonales.objects.get(legajo__id = self.id).apellido
        return f"{apellido}, {nombre} - {self.sector}"
    


