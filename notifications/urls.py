from django.urls import path
from .views import NotificationView, MarkNotificationReadView

urlpatterns = [
    path('', NotificationView.as_view(), name='notifications'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
]
