from django.contrib.auth.models import User
from django.db import models


class Ciudad(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Available(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "From: " + str(self.start_date) + " To: " + str(self.end_date)


class Cerrajero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Un cerrajero tiene una ciudad asignada... en una ciudad pueden vivir muchos cerrajeros
    city = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    serviceType = models.CharField(max_length=100)
    serviceObject = models.CharField(max_length=100)
    available = models.ManyToManyField(Available)
    # Numero de telefono
    phone = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.user.first_name


class Job(models.Model):
    # Usuario que hace el pedido del trabajo
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Cerrajero que hara el trabajo
    cerrajero = models.ForeignKey(Cerrajero, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50)
    service_object = models.CharField(max_length=50)
    # Si tiene que llevar la pieza si el servicio es cerradura
    take_piece = models.BooleanField(default=False)
    # Datos del carro si el servicio es Copia de llaves
    car_model = models.CharField(max_length=30, blank=True)
    car_year = models.CharField(max_length=30, blank=True)
    # Fecha a realizar el trabajo... fecha que se compara la disponibilidad
    date = models.DateField()
    status = models.CharField(default='Waiting', max_length=8,
                              choices=(('Waiting', 'Waiting'), ('Accepted', 'Accepted'), ('Canceled', 'Canceled')))
    # Por si tiene alguna cosa que sugerir
    description = models.CharField(max_length=500, blank=True)


class Rating(models.Model):
    cerrajero = models.ForeignKey(Cerrajero, on_delete=models.CASCADE)
    rate = models.IntegerField(null=False)

    def __hash__(self):
        return self.id
