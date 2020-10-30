from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User
from .serializers import *
from rest_framework.authtoken.models import Token


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    # def put(self, request, pk):
    #     user = User.objects.filter(id=pk)

        
