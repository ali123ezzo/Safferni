from django.db import models

# class Company(models.Model):
   
#    company_id = models.IntegerField(primary_key=True)
#    company_name = models.CharField(max_length=200)

#    def __str__(self):
#       return self.company_name

# class Bus(models.Model):
   
#    bus_id = models.IntegerField(primary_key=True)
#    company_id = models.ForeignKey(Company, on_delete=models.CASCADE) ####
#    Capacity = models.IntegerField()
#    number_of_seats_left = models.IntegerField(default=20)
#    VIP = models.BooleanField()

#    def __str__(self):
#       return f'{self.bus_id} - {self.company_id}'
   
# class Rout(models.Model):
   
#    rout_id = models.IntegerField(primary_key=True)
#    departure_location = models.CharField(max_length=200)
#    destination = models.CharField(max_length=200)
#    distance = models.DecimalField(max_digits=20, decimal_places=3)  

#    def __str__(self):
#       return self.departure_location + ' ' + self.destination 

# class Schedule(models.Model):
   
#    schedule_id = models.IntegerField(primary_key=True)
#    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True) ####
#    rout = models.ForeignKey(Rout, on_delete=models.SET_NULL, null=True) ####
#    date = models.DateField(default=datetime.now())
#    departure_time = models.TimeField()
#    arrivale_time = models.TimeField()

#    def __str__(self):
#       return f'{self.date} - {self.rout}'

# class Ticket(models.Model):
   
#    ticket_id = models.IntegerField(default=2)
#    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) ####  
#    booking_date = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True) ####
#    seat_number = models.IntegerField()
#    number_of_travelers = models.IntegerField()
#    total_price = models.DecimalField(decimal_places=3, max_digits=20)

#    def __str__(self):
#       return f'{self.ticket_id} - {self.user}'


# class User(AbstractUser):
   
#    user_id = models.AutoField(primary_key=True)
#    username = models.CharField(max_length=100, unique=True)
#    email = models.EmailField(max_length=200, unique=True)
#    password = models.CharField(max_length=200)
#    first_name = models.CharField(max_length=100)    
#    last_name = models.CharField(max_length=100)
#    phone_number = models.BigIntegerField(unique=True)

#    groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_name="buscompany_users_groups",  # Add a unique related_name
#         related_query_name="buscompany_user",
#    )
#    user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="buscompany_users_permissions",  # Add a unique related_name
#         related_query_name="buscompany_user",
#    )

#    USERNAME_FIELD = 'username'
#    REQUIRED_FIELDS = ['email', 'phone_number']

#    def __str__(self):
#       return self.first_name + ' ' + self.last_name
