from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from main.views import *

router = routers.SimpleRouter()
router.register('worker', WorkerViewSet, basename='worker')
router.register('vacation', VacationViewSet, basename='vacation')
router.register('gap', GapViewSet)
router.register('lateness', LatenessViewSet)
router.register('notification', NotificationViewSet, basename='notification')
router.register('enter', EnterViewSet)
router.register('exit', ExitViewSet)

urlpatterns = [
    path('registration/', registration),
    # path('users/<int:pk>/is_auth', is_auth),
    # path('check/', check),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
    path('worker/<int:pk>/vacations/', get_all_vacations),
    path('worker/<int:pk>/gaps/', get_all_gaps),
    path('worker/<int:pk>/latenesses/', get_all_latenesses),
    path('worker/<int:pk>/exits/', get_all_exits),
    path('worker/<int:pk>/enters/', get_all_enters),
    path('tables/', get_all_tables),
    path('send_code/', send_code),
    path('check_code/', check_reset_code),
    path('reset_password/', reset_password),
]

urlpatterns += router.urls


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
