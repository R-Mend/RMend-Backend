from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Authority, AuthorityIssueGroup, AuthorityIssue

@admin.register(Authority)
class AuthorityAdmin(OSMGeoAdmin):
    list_display = ('name', 'authority_type', 'address', 'phone_number', 'email', 'website_url')

@admin.register(AuthorityIssueGroup)
class AuthorityIssueGroupAdmin(OSMGeoAdmin):
    list_display = ('name', 'authority')

@admin.register(AuthorityIssue)
class AuthorityIssueAdmin(OSMGeoAdmin):
    list_display = ('name', 'issue_group')
