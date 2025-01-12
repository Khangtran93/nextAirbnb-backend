from django.contrib import admin

from .models import Property, Reservations

admin.site.register(Property)
admin.site.register(Reservations)
