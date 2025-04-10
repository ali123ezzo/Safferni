from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import Company, Bus, Booking
from .serializers import CompanySerializer, BusSerializer, BookingSerializer
from accounts.models import User
from rest_framework import serializers


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'ADMIN'

class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['STAFF', 'ADMIN']

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_name']

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.filter(is_active=True)
    serializer_class = BusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['source', 'destination', 'departure_date']
    search_fields = ['bus_number', 'source', 'destination']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsStaffOrAdmin]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = Bus.objects.filter(is_active=True)
        
        # Filter for available buses only for list view
        if self.action == 'list':
            source = self.request.query_params.get('source')
            destination = self.request.query_params.get('destination')
            date = self.request.query_params.get('departure_date')
            
            if source:
                queryset = queryset.filter(source__iexact=source)
            if destination:
                queryset = queryset.filter(destination__iexact=destination)
            if date:
                queryset = queryset.filter(departure_date=date)
            
            # Also show buses for nearby dates (+/- 1 day)
            if date and self.request.query_params.get('include_nearby', '').lower() == 'true':
                queryset = queryset.filter(
                    Q(departure_date=date) |
                    Q(departure_date__gte=date) |
                    Q(departure_date__lte=date)
                ).order_by('departure_date')
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        bus = self.get_object()
        booked_seats = bus.bookings.filter(is_cancelled=False).values_list('seat_number', flat=True)
        all_seats = range(1, bus.number_of_seats + 1)
        available_seats = [seat for seat in all_seats if seat not in booked_seats]
        return Response({'available_seats': available_seats})

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        if self.request.user.user_type in ['ADMIN', 'STAFF']:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        bus = serializer.validated_data['bus']
        seat_number = serializer.validated_data['seat_number']
        
        # Check if seat is already booked
        if Booking.objects.filter(bus=bus, seat_number=seat_number, is_cancelled=False).exists():
            raise serializers.ValidationError("This seat is already booked.")
        
        # Create booking
        booking = serializer.save()
        
        # Update remaining seats
        bus.remaining_seats -= 1
        bus.save()
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user and not request.user.user_type in ['ADMIN', 'STAFF']:
            return Response({'detail': 'You do not have permission to cancel this booking.'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        if booking.cancel():
            return Response({'status': 'Booking cancelled'})
        return Response({'status': 'Booking was already cancelled'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    