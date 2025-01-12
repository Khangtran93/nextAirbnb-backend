from rest_framework import serializers
from useraccount.serializers import UserDetailsSerializer
from .models import Property, Reservations

class PropertyListSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Property
    fields = (
      'id',
      'title',
      'price_per_night',
      'image_url', 
      'description'
    )

class PropertyDetailsSerializer(serializers.ModelSerializer):
  landlord = UserDetailsSerializer(read_only=True)
  class Meta:
    model = Property
    fields = (
      'id',
      'title',
      'description',
      'price_per_night',
      'bedrooms',
      'bathrooms',
      'guests',
      'country',
      'country_code',
      'image_url',
      'landlord'
    )

class ReservationDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reservations
    fields = ('id', 
              'property', 
              'start_date', 
              'end_data', 
              'number_of_nights', 
              'guests', 
              'total' 
    )