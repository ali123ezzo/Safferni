from django.utils import timezone
from django.db import models
from UserAuthAPI.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class BookingUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(default=timezone.now)
    number_of_seats = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:

        ordering = ['-booking_date']
        verbose_name_plural = "Bookings"

    def save(self,*args, **kwargs):

        # self.full_clean()
        if self.trip:
            self.total_price=self.number_of_seats * self.trip.price
        return super().save(*args, **kwargs)
    
    def cancel(self):

        if not self.is_cancelled:
            self.is_cancelled = True
            self.cancellation_date = timezone.now()
            self.trip.available_seats += self.number_of_seats
            self.trip.save()
            self.save()
            return True
        return False
    
    def clean(self):
        # Validate before saving
        if not self.is_cancelled:
            # Check if user already has an active booking for this bus
            existing_booking = BookingUser.objects.filter(
                user=self.user,
                trip=self.trip,
                is_cancelled=False
            ).exclude(pk=self.pk).exists()
            
            if existing_booking:
                raise ValidationError("You already have an active booking for this bus.")
            
            # Validate seat limit
            if self.number_of_seats > 8:
                raise ValidationError("Maximum 8 seats per booking.")
            
            if self.number_of_seats <= 0:
                raise ValidationError("Number of seats must be at least 1.")
            
            if self.number_of_seats > self.trip.available_seats:
                raise ValidationError(f"Only {self.trip.available_seats} seat(s) available.")
            
    def delete(self, *args, **kwargs):

        if not self.is_cancelled:
            self.trip.available_seats += self.number_of_seats
            self.trip.save()
        super().delete(*args, **kwargs)
            
    def __str__(self):
        
        return f"Booking: {self.user.username} for {self.trip} (Seat {self.number_of_seats})"
    

