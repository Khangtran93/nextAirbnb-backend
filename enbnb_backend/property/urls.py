from django.urls import path
from . import api

urlpatterns = [
  path('', api.property_list, name="api_properties_list"),
  path('create/', api.create_property, name='api_create_property'),
  path('<uuid:pk>/', api.get_property_details, name='api_get_property'),
  path('<uuid:pk>/book/', api.create_reservation, name='api_create_reservation'),
  path('<uuid:pk>/reservations/', api.get_property_reservations, name='api_get_property_reservation'),
  path('reservations/', api.get_user_reservations, name='api_get_user_reservations'),
  path('favorites/', api.get_favorite_properties, name='api_get_favorite_properties'),
]