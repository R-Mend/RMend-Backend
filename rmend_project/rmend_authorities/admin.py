from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Authority, AuthorityIssueTypeGroup, AuthorityIssueType, BaseIssueTypeGroup, BaseIssueType

from django.contrib.gis.db import models
from django.forms.widgets import Textarea

@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'authority_type', 'address', 'phone_number', 'email', 'website_url')
    formfield_overrides = {
        models.PolygonField: {'widget': Textarea }
    }

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