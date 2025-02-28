from rest_framework import serializers
from useraccount.serializers import UserDetailsSerializer
from .models import Property, PropertyImage, Reservations

class PropertyListSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Property
    fields = (
      'id',
      'title',
      'price_per_night',
      # 'image_url', 
      'description'
    )

class PropertyImageListSerializer(serializers.ModelSerializer):
  class Meta:
    model = PropertyImage
    fields = (
        'id', 
        'image', 
        'property_id'
    )

class PropertyDetailsSerializer(serializers.ModelSerializer):
  landlord = UserDetailsSerializer(read_only=True)
  images = PropertyImageListSerializer(many=True, read_only=True)
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
              # 'image_url',
              'landlord',
              'images'
    )

class ReservationListSerializer(serializers.ModelSerializer):
  property = PropertyDetailsSerializer(read_only=True)
  customer = UserDetailsSerializer(read_only=True)
  class Meta:
    model = Reservations
    fields = ('id', 
              'property', 
              'customer', 
              'total',
              'start_date', 
              'end_date',
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

class PropertyImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = PropertyImage
    fields = ('id')