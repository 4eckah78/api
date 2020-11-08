from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from main.views import *

router = routers.SimpleRouter()
router.register('worker', WorkerViewSet)
router.register('vacation', VacationViewSet)
router.register('gap', GapViewSet)
router.register('lateness', LatenessViewSet)
router.register('notification', NotificationViewSet)
router.register('enter', EnterViewSet)
router.register('exit', ExitViewSet)

urlpatterns = [
    path('registration/', registration),
    # path('users/<int:pk>/is_auth', is_auth),
    # path('check/', check),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
]

urlpatterns += router.urls


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
