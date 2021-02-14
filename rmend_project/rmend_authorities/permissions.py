from rest_framework import permissions

class IsAuthorityAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Checks if the user is a part of the authority they're trying to access"""
        if hasattr(obj, 'authority'):
            admin_users = obj.authority.admin_users
        else:
            admin_users = obj.admin_users
        return request.user in admin_users.all()
