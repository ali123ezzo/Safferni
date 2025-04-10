from django.db import models

# Create your models here.


class Company(models.Model):
   
   company_name = models.CharField(max_length=200)
   logo = models.ImageField(upload_to='company_logo', null=True, blank=True)

   def __str__(self):
      return self.company_name
   