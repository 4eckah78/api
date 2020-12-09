from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *

User = get_user_model()



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
        extra_kwargs = {'first_name':{"required": True}, 'last_name':{"required": True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name = validated_data["last_name"],
            table_name = validated_data["table_name"],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"


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


class WorkerSerializer(serializers.ModelSerializer):
    vacations = VacationSerializer(many=True, read_only=True)
    gaps = GapSerializer(many=True, read_only=True)
    latenesses = LatenessSerializer(many=True, read_only=True)
    exits = ExitSerializer(many=True, read_only=True)
    enters = EnterSerializer(many=True, read_only=True)
    class Meta:
        model = Worker
        fields = ["id", "first_name", "second_name", "patronymic", "avatar", 
        "hour_norm", "vacation_days", "start_day", "end_day", "vacations", "gaps", "latenesses", "exits", "enters"]
        extra_kwargs = {'vacations':{"required": False}, 'gaps':{"required": False}, 'latenesses':{"required": False},
        'exits':{"required": False}, 'enters':{"required": False} }


class UserListSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True)
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_superuser", "table_name", "notifications", "workers"]
        extra_kwargs = {'email':{"required": False}, 'table_name':{"required": False} }


class TablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["table_name"]