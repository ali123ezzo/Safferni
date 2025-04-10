from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USER_TYPES = (
        ('ADMIN', 'ADMIN'),
        ('STAFF', 'STAFF'),
        ('CUSTOMER', 'CUSTOMER'),
    )
    
    phone_number = PhoneNumberField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='CUSTOMER')
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email']

    def __str__(self):
        return self.username