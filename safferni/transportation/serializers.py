from rest_framework import serializers
from .models import Company, Bus, Booking
from .models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class BusSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    
    class Meta:
        model = Bus
        fields = '__all__'
        read_only_fields = ('remaining_seats', 'created_at', 'updated_at')

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    bus_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_date', 'is_cancelled', 'cancellation_date')
    
    def get_bus_details(self, obj):
        return {
            'bus_number': obj.bus.bus_number,
            'source': obj.bus.source,
            'destination': obj.bus.destination,
            'departure_date': obj.bus.departure_date,
            'departure_time': obj.bus.departure_time,
            'price': obj.bus.price
        }
    
    def validate(self, data):
        bus = data['bus']
        if bus.remaining_seats <= 0:
            raise serializers.ValidationError("No available seats on this bus.")
        return data