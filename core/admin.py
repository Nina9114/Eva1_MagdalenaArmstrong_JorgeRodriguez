from django.contrib import admin
from .models import Organization, UserProfile, Category, Zone, Device, Measurement, Alert

admin.site.register([Organization, UserProfile, Category, Zone, Device, Measurement, Alert])

