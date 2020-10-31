from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import *


urlpatterns = [
    path('registration/', registration),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
