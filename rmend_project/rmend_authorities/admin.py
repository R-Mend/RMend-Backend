from django.contrib import admin
from django.contrib.gis.db import models
from django.forms.widgets import Textarea

from .models import (Authority, AuthorityIssueTypeGroup, AuthorityIssueType, 
    BaseIssueTypeGroup, BaseIssueType)


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    """Admin console representation of the Authority model"""
    list_display = ('name', 'authority_type', 'address', 'phone_number', 'email', 'website_url')
    formfield_overrides = {
        models.PolygonField: {'widget': Textarea }
    }

@admin.register(AuthorityIssueTypeGroup)
class AuthorityIssueGroupAdmin(admin.ModelAdmin):
    """Admin console representation of the AuthorityIssueTypeGroup model"""
    list_display = ('name', 'authority')

@admin.register(AuthorityIssueType)
class AuthorityIssueAdmin(admin.ModelAdmin):
    """Admin console representation of the AuthorityIssueTyoe model"""
    list_display = ('name', 'issue_group')

@admin.register(BaseIssueTypeGroup)
class BaseIssueTypeGroupAdmin(admin.ModelAdmin):
    """Admin console representation of the BaseIssueTypeGroup model"""
    list_display = ('name',)

@admin.register(BaseIssueType)
class BaseIssueTypeAdmin(admin.ModelAdmin):
    """Admin console representation of the BaseIssueType model"""
    list_display = ('name', 'issue_group')
