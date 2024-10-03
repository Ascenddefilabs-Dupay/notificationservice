# from django.urls import path
# from .views import GetMessagesUserIds, CreateMessagesNotificationView

# urlpatterns = [
#     path('get-messages-user-ids/', GetMessagesUserIds.as_view(), name='get-messages-user-ids'),
#     path('create-messages/', CreateMessagesNotificationView.as_view(), name='create-messages'),
# ]

# urls.py
from django.urls import path
from .views import (
    GetMessagesUserIds,
    CreateMessagesNotificationView,
    AdminMessagesListCreateView,
    AdminMessagesUpdateDeleteView,
)

urlpatterns = [
    path('get-messages-user-ids/', GetMessagesUserIds.as_view(), name='get-messages-user-ids'),
    path('create-messages/', CreateMessagesNotificationView.as_view(), name='create-messages-notification'),
    path('admin-messages/', AdminMessagesListCreateView.as_view(), name='admin-messages-list-create'),
    path('admin-messages/<str:content_id>/', AdminMessagesUpdateDeleteView.as_view(), name='admin-messages-update-delete'),
]
