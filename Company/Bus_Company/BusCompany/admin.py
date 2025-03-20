from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Schedule)
admin.site.register(Ticket)
admin.site.register(Bus)
admin.site.register(Rout)
admin.site.register(Company)
