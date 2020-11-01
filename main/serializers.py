from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_superuser", "table_name"]
        extra_kwargs = {'email':{"required": False}, 'table_name':{"required": False} }


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        

class MyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["user", "key"]