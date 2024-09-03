from django.urls import path
from .views import GetAccountActivityUserIds, CreateAccountActivityNotificationView

urlpatterns = [
    path('get-account-activity-user-ids/', GetAccountActivityUserIds.as_view(), name='get-account-activity-user-ids'),
    path('create-account-activity/', CreateAccountActivityNotificationView.as_view(), name='create-account-activity'),
]
