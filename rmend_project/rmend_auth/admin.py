from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = 'user'

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline, )

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
