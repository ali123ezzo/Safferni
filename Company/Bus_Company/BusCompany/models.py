from datetime import datetime
from django.db import models

# Create your models here.

class Company(models.Model):
   
   company_id = models.IntegerField(primary_key=True)
   company_name = models.CharField(max_length=200)

   def __str__(self):
      return self.company_name

class Bus(models.Model):
   
   bus_id = models.IntegerField(primary_key=True)
   company_id = models.ForeignKey(Company, on_delete=models.CASCADE) ####
   Capacity = models.IntegerField()
   number_of_seats_left = models.IntegerField(default=20)
   VIP = models.BooleanField()

   def __str__(self):
      return f'{self.bus_id} - {self.company_id}'
   
class User(models.Model):
   
   user_id = models.IntegerField(primary_key=True)
   user_name = models.CharField(max_length=100)
   password = models.CharField(max_length=200)
   first_name = models.CharField(max_length=100)    
   last_name = models.CharField(max_length=100)
   phone_number = models.BigIntegerField()

   def __str__(self):
      return self.first_name + ' ' + self.last_name

class Rout(models.Model):
   
   rout_id = models.IntegerField(primary_key=True)
   departure_location = models.CharField(max_length=200)
   destination = models.CharField(max_length=200)
   distance = models.DecimalField(max_digits=20, decimal_places=3)  

   def __str__(self):
      return self.departure_location + ' ' + self.destination 

class Schedule(models.Model):
   
   schedule_id = models.IntegerField(primary_key=True)
   bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True) ####
   rout = models.ForeignKey(Rout, on_delete=models.SET_NULL, null=True) ####
   date = models.DateField(default=datetime.now())
   departure_time = models.TimeField()
   arrivale_time = models.TimeField()

   def __str__(self):
      return f'{self.date} - {self.rout}'

class Ticket(models.Model):
   
   ticket_id = models.IntegerField(default=2)
   user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) ####  
   booking_date = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True) ####
   seat_number = models.IntegerField()
   number_of_travelers = models.IntegerField()
   total_price = models.DecimalField(decimal_places=3, max_digits=20)

   def __str__(self):
      return f'{self.ticket_id} - {self.user}'
