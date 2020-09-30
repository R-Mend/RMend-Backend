from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Authority

@admin.register(Authority)
class AuthorityAdmin(OSMGeoAdmin):
    list_display = ('name', 'authority_type', 'adress', 'phone_number', 'email', 'website_url')