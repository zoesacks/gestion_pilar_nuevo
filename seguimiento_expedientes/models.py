from django.db   import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from configuracion.models import TipoDocumento
from recursos_humanos.models import Legajo

class Transferencia(models.Model):
    #Obligatorios
    fecha = models.DateField(blank=False)
    emisor = models.ForeignKey(Legajo, on_delete=models.CASCADE, related_name="emisor")
    receptor = models.ForeignKey(Legajo, on_delete=models.CASCADE, related_name="receptor")
    fecha_confirmacion = models.DateField(blank=True, null=True)

    #extra
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.fecha}. Emisor: {self.emisor}. Receptor: {self.receptor}'
    
    class Meta:
        verbose_name = 'transferencia'
        verbose_name_plural ='Transferencias'

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        super(Transferencia, self).save(*args, **kwargs)


class Documento(models.Model):
    #DATOS DEL DOCUMENTO
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numero = models.IntegerField()
    ejercicio = models.CharField(max_length = 4)
    propietario = models.ForeignKey(Legajo, on_delete=models.CASCADE, related_name="propietario")
    #se autocompleta
    fecha_alta = models.DateField(auto_now_add=True, blank=True, null=True)
    
    
    #PARA CUANDO EL DOCUMENTO ESTA EN TRANSFERIA
    #obligatorio
    destinatario = models.ForeignKey(Legajo, on_delete=models.CASCADE, blank=True, null=True, related_name="destinatario")

    #extra
    observacion = models.TextField(blank=True, null=True)

    #se autocompleta con el formulario
    en_transito = models.BooleanField(default=False)
    fecha_transito = models.DateField(blank=True, null=True)


    #HITORIAL DE TRANSFERENCIAS
    transferencias = models.ManyToManyField(Transferencia)

    def __str__(self):
        return f'{self.tipo.descripcion}. Nro:  {self.tipo}-{self.numero},  {self.ejercicio}'
    
    class Meta:
        verbose_name = 'documento'
        verbose_name_plural ='Documentos'

    def clean(self):
        if self.existe():
            raise ValidationError("El documento ya esta registrado en el sistema")
        super().clean() 


    def transferir(self, destinatario, observacion):
        self.validar_transferencia(destinatario)
        
        self.destinatario = destinatario
        self.observacion = observacion if observacion else None
        self.en_transito = True
        self.fecha_transito = timezone.now()

        self.save()

    def confirmarTransferencia(self):
        self.validar_confirmarTransferencia()

        transferencia = Transferencia.objects.create(
            fecha=self.fecha_transito,
            emisor=self.propietario,
            receptor=self.destinatario,
            fecha_confirmacion=timezone.now(),
            observacion=self.observacion if self.observacion else None
        )

        self.transferencias.add(transferencia)
        self.propietario = self.destinatario
        self.destinatario = None
        self.observacion = None
        self.en_transito = False
        self.fecha_transito = None

        self.save()


    def validar_transferencia(self, destinatario):
        if destinatario == self.propietario:
            raise ValidationError("No se pueden hacer transferencias a ti mismo")
        if self.en_transito == True:
            raise ValidationError("El documento ya se encuentra en transito")
        

    def validar_confirmarTransferencia(self):
        if self.en_transito == False:
            raise ValidationError("El documento no se encuentra en transito")
        if self.destinatario == False:
            raise ValidationError("El documento no tiene destinatario")

    def existe(self):
        return Documento.objects.filter(tipo = self.tipo, numero = self.numero, ejercicio = self.ejercicio).exclude(pk=self.pk).exists()
    




