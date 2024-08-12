# Pushnotification1/urls.py
from django.urls import path
from .views import CreateNotificationView, NotificationListView

urlpatterns = [
    path('api2/create-notification/', CreateNotificationView.as_view(), name='create-notification'),
    path('api2/notifications/', NotificationListView.as_view(), name='notification-list'),
    # path('create-notification/', views.create_notification, name='create_notification'),
]
