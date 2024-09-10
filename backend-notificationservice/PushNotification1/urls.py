from django.urls import path
from .views import GetMessagesUserIds, CreateMessagesNotificationView

urlpatterns = [
    path('get-messages-user-ids/', GetMessagesUserIds.as_view(), name='get-messages-user-ids'),
    path('create-messages/', CreateMessagesNotificationView.as_view(), name='create-messages'),
]
