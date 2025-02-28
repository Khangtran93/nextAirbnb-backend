from django.forms import ModelForm

from .models import Property

class PropertyModelForm(ModelForm):
  class Meta:
    model = Property
    fields = ('category', 
              'title', 
              'description', 
              'price_per_night', 
              'bedrooms', 
              'bathrooms', 
              'guests', 
              'country', 
              'country_code', 
              )