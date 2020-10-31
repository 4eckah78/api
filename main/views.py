from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError 
from  django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, HttpResponse
from .models import User
from .serializers import *
from .permissions import IsOwnerOrReadOnlyOrIsAdmin, IsSuperuser


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperuser, ]


class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnlyOrIsAdmin, ]


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError as e:
            return Response({"error" : e.message})
        password = request.POST['password']
        try: 
            validate_password(password)
        except ValidationError as e:
            return Response({"error" : e.messages}) 
        try: 
            userid = User.objects.create_user(email=email, password=password).id
        except IntegrityError as e:
            if "1062" in str(e):
                return Response({"error": "Такой email уже существует"})
            returnResponse({"error": "Что-то пошло не так. Возможно введенный email уже существует"})
        return Response({"id": userid, "token": Token.objects.get(user=userid).key})
