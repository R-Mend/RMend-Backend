from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Report

class ReportAdmin(OSMGeoAdmin):
    list_display = ('authority', 'report_type', 'date_created', 'nearest_address')
    readonly_fields = ('authority', 'report_type', 'location', 'details', 'nearest_address', 
        'date_created', 'sender_email', 'sender_name', 'sender_phone')

admin.site.register(Report, ReportAdmin)