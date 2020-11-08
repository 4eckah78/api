from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_superuser", "table_name", "notifications"]
        extra_kwargs = {'email':{"required": False}, 'table_name':{"required": False} }


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
 

class MyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["user", "key"]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "table_name"]
        extra_kwargs = {'first_name':{"required": True}, 'last_name':{"required": True} }


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "first_name", "second_name", "patronymic", "avatar_path", 
        "hour_norm", "vacation_days", "user", "vacations", "gaps", "latenesses", "exits", "enters"]


class GapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gap
        fields = "__all__"


class LatenessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lateness
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class ExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exit
        fields = "__all__"


class EnterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enter
        fields = "__all__"
