import random
import datetime
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from django.http import QueryDict
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.db import IntegrityError 
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, HttpResponse
from .models import User
from .serializers import *
from .permissions import *
from .common import get_all_worker_data


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    # permission_classes = (IsAdmin, )


class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]
    def get(self, request, pk):
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        if year == None or month == None:
            return Response(data={"error":"no year or month in url"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, id=pk)
        workers_q = Worker.objects.filter(user=user)
        workers = []
        for worker in workers_q:
            exits = Exit.objects.filter(worker=worker, time__year=year, time__month=month).order_by('time')
            enters = Enter.objects.filter(worker=worker, time__year = year, time__month=month).order_by('time')
            gaps = Gap.objects.filter(worker=worker, date__year = year, date__month=month)
            ex_serializer = ExitSerializer(exits, many=True)
            en_serializer = EnterSerializer(enters, many=True)
            gap_serializer = GapSerializer(gaps, many=True)
            w_serializer = WorkerCreateSerializer(worker, many=False)
            filter_data = dict(w_serializer.data)
            filter_data["exits"] = ex_serializer.data
            filter_data["enters"] = en_serializer.data
            filter_data["gaps"] = gap_serializer.data
            workers.append(filter_data)

        notifications_q = Notification.objects.filter(user=user)
        notifications = []
        for notification in notifications_q:
            n_serializer = NotificationSerializer(notification, many=False)
            filter_data = dict(n_serializer.data)
            if notification.is_gap:
                filter_data["worker"] = notification.gap.worker.id
                filter_data["date"] = notification.gap.date
            else:
                filter_data["worker"] = notification.lateness.worker.id
                filter_data["date"] = notification.lateness.time_of_lateness
            notifications.append(filter_data)
        
        serializer = self.serializer_class(user)
        data = dict(serializer.data)
        data["workers"] = workers
        data["notifications"] = notifications
        
        return Response(data, status=status.HTTP_200_OK)


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.workers.all()
        return Worker.objects.all()
    def create(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = QueryDict('', mutable=True)
        data.update({"user": request.user.id})
        data.update(request.data)
        serializer = WorkerCreateSerializer(data=data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VacationViewSet(viewsets.ModelViewSet):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
    # permission_classes = [IsOwnerOrReadOnlyAndNoUserField, IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Vacation.objects.filter(worker__user=self.request.user)
        return Vacation.objects.all()
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        vacation = Vacation.objects.get(id=serializer.data["id"])
        worker = Worker.objects.get(id=vacation.worker.id)
        vac = vacation.end_date - vacation.start_date
        if vac.days + 1 > worker.vacation_days:
            vacation.delete()
            return Response({"error":"this worker hasn't so many vacations"}, status=status.HTTP_400_BAD_REQUEST)
        worker.vacation_days -= vac.days + 1
        worker.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(('GET',))
def get_all_vacations(request, pk):
    return get_all_worker_data(request, pk, Vacation, VacationSerializer)


class GapViewSet(viewsets.ModelViewSet):
    serializer_class = GapSerializer
    queryset = Gap.objects.all()
    # permission_classes = [IsOwnerOrReadOnlyAndNoUserField, IsAuthenticatedOrReadOnly]
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        worker = Worker.objects.get(id=serializer.data["worker"])
        gap = Gap.objects.get(id=serializer.data["id"])
        notification = Notification.objects.create(user=worker.user, gap=gap, is_gap=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def get_all_gaps(request, pk):
    return get_all_worker_data(request, pk, Gap, GapSerializer)


class LatenessViewSet(viewsets.ModelViewSet):
    serializer_class = LatenessSerializer
    queryset = Lateness.objects.all()
    # permission_classes = [IsOwnerOrReadOnlyAndNoUserField, IsAuthenticatedOrReadOnly]


@api_view(('GET',))
def get_all_latenesses(request, pk):
    return get_all_worker_data(request, pk, Lateness, LatenessSerializer)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.notifications.all()
        return Notification.objects.all()


class ExitViewSet(viewsets.ModelViewSet):
    serializer_class = ExitSerializer
    queryset = Exit.objects.all()
    # permission_classes = [IsOwnerOrReadOnlyAndNoUserField, IsAuthenticatedOrReadOnly]


@api_view(('GET',))
def get_all_exits(request, pk):
    return get_all_worker_data(request, pk, Exit, ExitSerializer)



class EnterViewSet(viewsets.ModelViewSet):
    serializer_class = EnterSerializer
    queryset = Enter.objects.all()
    # permission_classes = [IsOwnerOrReadOnlyAndNoUserField, IsAuthenticatedOrReadOnly]
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        worker = Worker.objects.get(id=serializer.data["worker"])
        if serializer.data["time"][11:19] > str(worker.start_day):
            lateness = Lateness.objects.create(worker=worker, time_of_lateness=serializer.data["time"])
            notification = Notification.objects.create(user=worker.user, lateness=lateness, is_gap=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def get_all_enters(request, pk):
    return get_all_worker_data(request, pk, Enter, EnterSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    user = User.objects.get(email=serializer.data["email"])
    token = Token.objects.get(user=user).key
    return Response(data={"id":user.id, "is_superuser":user.is_superuser, "token":token}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    email = request.data["email"]
    user = get_object_or_404(User, email=email)
    code = random.randint(10000,100000)
    user.password = code
    user.save()
    result = send_mail("Attendance Control, восстановление пароля",
              "Код подтверждения: " + str(code),
              "Attendance Control <noreply@attendancecontrol.com>",
              [email],
              fail_silently=False)
    if result == 0:
        return Response(data={"error":"email was not sent. Maybe the email address doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"message":"email is successfully sent"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_reset_code(request):
    code = request.data["code"]
    user = get_object_or_404(User, password=code)
    token, created = Token.objects.get_or_create(user=user)
    return Response(data={"token":token.key, "id":token.user.id}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def reset_password(request):
    password = request.data["password"]
    user = request.user
    user.set_password(password)
    user.save()
    return Response(data={"message":"password is successfully changed"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_all_tables(request):
    users = User.objects.all()
    serializer = TablesSerializer(users, many=True)
    tables = [user["table_name"] for user in serializer.data]
    return Response(data=tables, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def is_auth(request, pk):
#     return Response({"isAuthenticated": len(Token.objects.filter(user=pk))})

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def check(request):
#     return Response({"isAuthenticated": request.user.is_authenticated})