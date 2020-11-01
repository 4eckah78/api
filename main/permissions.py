from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .models import User


class IsOwnerOrReadOnlyOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        if len(Token.objects.filter(user=obj.id)) == 0:
            return false 
        obj_token = Token.objects.get(user=obj.id).key
        request_token = request.headers['Authorization'][6:]
        return obj_token == request_token


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
     