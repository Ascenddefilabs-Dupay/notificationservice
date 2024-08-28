
from django.urls import path
from .views import CreateNotificationView, NotificationListView, get_user_ids

urlpatterns = [
    path('create-notification/', CreateNotificationView.as_view(), name='create-notification'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('get-user-ids/', get_user_ids, name='get-user-ids'),
]
