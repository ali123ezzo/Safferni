from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


User = get_user_model()

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logo', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Bus(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='buses')
    bus_number = models.CharField(max_length=20, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    remaining_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    estimated_arrival_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus_number} - {self.source} to {self.destination}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new buses
            self.remaining_seats = self.number_of_seats
        super().save(*args, **kwargs)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('bus', 'seat_number')

    def __str__(self):
        return f"Booking #{self.id} - Seat {self.seat_number} on {self.bus}"

    def cancel(self):
        if not self.is_cancelled:
            self.is_cancelled = True
            self.cancellation_date = timezone.now()
            self.bus.remaining_seats += 1
            self.bus.save()
            self.save()
            return True
        return False

    