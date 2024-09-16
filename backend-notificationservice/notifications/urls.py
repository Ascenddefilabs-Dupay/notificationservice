# notifications/urls.py
from django.urls import path
from .views import fetch_notifications

urlpatterns = [
    path('fetch-notifications/', fetch_notifications, name='fetch_notifications'),
]
