from django.contrib import admin
from .models import Company, Bus, Booking

# Register your models here.


admin.site.register(Company)
admin.site.register(Bus)
admin.site.register(Booking)

