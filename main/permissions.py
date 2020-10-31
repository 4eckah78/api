from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .models import User


class IsOwnerOrReadOnlyOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        obj_token = Token.objects.filter(user=obj.id)
        request_token = request.headers['Authorization'][6:]
        return obj_token == request_token


class IsSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
     