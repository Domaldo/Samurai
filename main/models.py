from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
    Nueva tabla extra donde se registran las ciudades
"""


# class Ciudad(models.Model):
    # nombre = models.CharField(max_length=30)

    # def __str__(self):
        # return self.nombre


class Cerrajero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Un cerrajero tiene una ciudad asignada... en una ciudad pueden vivir muchos cerrajeros
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)

    # Numero de telefono
    phone = models.CharField(null=True, max_length=10)

    # Tipo de Servicio
    serviceType = models.CharField(null=True, blank=True, max_length=40)

    # Objeto de Servicio
    serviceObject = models.CharField(null=True, blank=True, max_length=40)

    # Urgencia del Servicio
    serviceUrgency = models.CharField(null=True, blank=True, max_length=40)

    # Intencion del Servicio
    serviceIntent = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.user.first_name


class Rating(models.Model):
    cerrajero = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(null=False)

    def __hash__(self):
        return self.id
