from email.policy import default
import uuid
from django.conf import settings
from django.db import models

from useraccount.models import User

class Property(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  description = models.TextField()
  price_per_night = models.IntegerField()
  bedrooms = models.IntegerField()
  bathrooms = models.IntegerField()
  guests = models.IntegerField()
  country = models.CharField(max_length=255)
  country_code = models.CharField(max_length=255)
  category = models.CharField(max_length=255)
  # image = models.ImageField(upload_to='uploads/properties')
  landlord = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  # def image_url(self):
  #   return f'{settings.WEBSITE_URL}{self.image.url}'
  

class Reservations(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  property = models.ForeignKey(Property, related_name="reservations", on_delete=models.CASCADE)
  total = models.FloatField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  number_of_nights = models.IntegerField()
  guest = models.IntegerField()
  customer = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
  create_at = models.DateTimeField(auto_now_add=True)

class PropertyImage(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
  image = models.ImageField(upload_to='uploads/properties')
  upload_at = models.DateTimeField(auto_now_add=True, null=True)