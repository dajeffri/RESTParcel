from rest_framework import permissions
from data.models import Company, MailPiece

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

class IsCompany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.company == request.user.profile.company)

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user)
