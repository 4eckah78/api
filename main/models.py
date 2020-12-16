from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from .managers import UserManager
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    table_name = models.CharField(max_length=60, unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Отправляет электронное письмо этому пользователю.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Worker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="workers") 
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    HOUR_NORM = (
        (1, 36),
        (2, 40),
    )
    hour_norm = models.IntegerField(choices=HOUR_NORM)
    vacation_days = models.PositiveSmallIntegerField()
    start_day = models.TimeField()
    end_day = models.TimeField()


class Lateness(models.Model):
    worker = models.ForeignKey(Worker, related_name="latenesses", on_delete = models.CASCADE)
    time_of_lateness = models.DateTimeField(default=timezone.now)
   

class Gap(models.Model):
    worker = models.ForeignKey(Worker, related_name="gaps", on_delete = models.CASCADE)
    date = models.DateField(default=timezone.now)
    REASONS = (
        (1, "Выходной"),
        (2, "Больничный"),
        (3, "Отпуск"),
        (4, "Командировка"),
    )
    reason = models.IntegerField(choices=REASONS) 
    document = models.ImageField(upload_to='media/documents/', null=True, blank=True)


class Notification(models.Model):
    is_gap = models.BooleanField()
    lateness = models.OneToOneField(Lateness, on_delete=models.CASCADE, null=True, blank=True)
    gap = models.OneToOneField(Gap, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete = models.CASCADE)


class Vacation(models.Model):
    worker = models.ForeignKey(Worker, related_name="vacations", on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Exit(models.Model):
    worker = models.ForeignKey(Worker, related_name="exits", on_delete = models.CASCADE)
    time = models.DateTimeField(default=timezone.now)


class Enter(models.Model):
    worker = models.ForeignKey(Worker, related_name="enters", on_delete = models.CASCADE)
    time = models.DateTimeField(default=timezone.now)


@receiver(post_delete, sender=Notification)
def auto_delete_lateness_and_gap_with_notification(sender, instance, **kwargs):
    if not instance.is_gap:
        instance.lateness.delete()
