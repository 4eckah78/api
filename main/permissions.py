from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
     

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.method != 'GET':
            return True
        return obj.user == request.user


class IsOwnerOrReadOnlyAndNoUserField(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.method != 'GET':
            return True
        return obj.worker.user == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.method != 'GET':
            return True
        return obj == request.user