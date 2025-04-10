from django.db import models

# Create your models here.


class Bus(models.Model):

    bus_identification_number = models.IntegerField()
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    number_of_seats = models.DecimalField(decimal_places=0, max_digits=2)
    remaimning_seats = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.bus_name
