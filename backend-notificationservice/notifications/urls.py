from django.urls import path
from .views import notification_list, unread_notification_count, mark_as_read

urlpatterns = [
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/unread-count/', unread_notification_count, name='unread_notification_count'),
    path('notifications/mark-as-read/<str:notification_id>/', mark_as_read, name='mark_as_read'),
]
