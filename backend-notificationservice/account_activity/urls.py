# urls.py
from django.urls import path
from .views import (
    GetAccountActivityUserIds,
    CreateAccountActivityNotificationView,
    AdminAccountActivityListCreateView,
    AdminAccountActivityUpdateDeleteView,
)

urlpatterns = [
    path('get-account-activity-user-ids/', GetAccountActivityUserIds.as_view(), name='get-account-activity-user-ids'),
    path('create-account-activity/', CreateAccountActivityNotificationView.as_view(), name='create-account-activity-notification'),
    path('admin-account-activity/', AdminAccountActivityListCreateView.as_view(), name='admin-account-activity-list-create'),
    path('admin-account-activity/<str:content_id>/', AdminAccountActivityUpdateDeleteView.as_view(), name='admin-account-activity-update-delete'),
]
