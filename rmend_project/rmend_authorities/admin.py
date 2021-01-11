from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Authority, AuthorityIssueTypeGroup, AuthorityIssueType, BaseIssueTypeGroup, BaseIssueType

@admin.register(Authority)
class AuthorityAdmin(OSMGeoAdmin):
    list_display = ('name', 'authority_type', 'address', 'phone_number', 'email', 'website_url')

@admin.register(AuthorityIssueTypeGroup)
class AuthorityIssueGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'authority')

@admin.register(AuthorityIssueType)
class AuthorityIssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'issue_group')

@admin.register(BaseIssueTypeGroup)
class BaseIssueTypeGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BaseIssueType)
class BaseIssueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'issue_group')