from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.db import IntegrityError 
from  django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, HttpResponse
from .models import User
from .serializers import *
from .permissions import IsOwnerOrReadOnly, IsAdmin


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, )


class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, )


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class VacationViewSet(viewsets.ModelViewSet):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()


class GapViewSet(viewsets.ModelViewSet):
    serializer_class = GapSerializer
    queryset = Gap.objects.all()


class LatenessViewSet(viewsets.ModelViewSet):
    serializer_class = LatenessSerializer
    queryset = Lateness.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


class ExitViewSet(viewsets.ModelViewSet):
    serializer_class = ExitSerializer
    queryset = Exit.objects.all()


class EnterViewSet(viewsets.ModelViewSet):
    serializer_class = EnterSerializer
    queryset = Enter.objects.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    # email = request.POST['email']
    # password = request.POST['password']
    # try: 
    #     validate_password(password)
    # except ValidationError as e:
    #     return Response({"error" : e.messages}) 
    # serializer.validated_data["password"] = password
    serializer.save()
    user = User.objects.get(email=serializer.data["email"])
    token = Token.objects.get(user=user).key
    return Response(data={"id":user.id, "token":token}, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def is_auth(request, pk):
#     return Response({"isAuthenticated": len(Token.objects.filter(user=pk))})

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def check(request):
#     return Response({"isAuthenticated": request.user.is_authenticated})