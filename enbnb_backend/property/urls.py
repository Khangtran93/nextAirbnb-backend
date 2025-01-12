from django.urls import path
from . import api

urlpatterns = [
  path('', api.property_list, name="api_properties_list"),
  path('create/', api.create_property, name='api_create_property'),
  path('<uuid:pk>/', api.get_property, name='api_get_property'),
  path('<uuid:pk>/book/', api.create_reservation, name='api_create_reservation'),
]