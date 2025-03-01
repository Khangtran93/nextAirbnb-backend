from django.contrib import admin

from .models import Property, PropertyImage, Reservations


admin.site.register(Property)
admin.site.register(Reservations)
admin.site.register(PropertyImage)
