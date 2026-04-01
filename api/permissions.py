from rest_framework import permissions


# just checking if the logged in user has the right role
# I could probably combine some of these but keeping them separate is cleaner

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsAnalystUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ANALYST'


class IsViewerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'VIEWER'


class CanManageRecords(permissions.BasePermission):
    """
    Admin can do everything.
    Analyst can only read (GET, HEAD, OPTIONS).
    Viewer gets 403 on everything.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'ADMIN':
            return True

        # analyst can read but not write
        if request.user.role == 'ANALYST' and request.method in permissions.SAFE_METHODS:
            return True

        return False
