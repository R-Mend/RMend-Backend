from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Report

class ReportAdmin(OSMGeoAdmin):
    list_display = [field.name for field in Report._meta.get_fields()]
    # list_display = ('authority', 'location', 'details', 'date_created', 'report_type', 'nearest_address')

admin.site.register(Report, ReportAdmin)