from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    
    phone_number = PhoneNumberField()
    password2 = models.CharField(max_length=300, blank=False, null=False)
    
# class User(AbstractUser):
   
#    user_id = models.AutoField(primary_key=True)
#    username = models.CharField(max_length=100, unique=True)
#    email = models.EmailField(unique=True)
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
