from rest_framework import permissions

class IsAuthorityAdmin(permissions.BasePermission):
    """Permission class for object level access to authorites admin esers only"""

    def has_object_permission(self, request, view, obj):
        """Checks if the user is a part of the authority they're trying to access"""
        admin_users = obj.authority.admin_users
        return request.user in admin_users.all()
