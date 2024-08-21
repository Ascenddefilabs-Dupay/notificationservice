# account_activity/urls.py
from django.urls import path
from .views import CreateAccountActivityNotificationView, AccountActivityNotificationListView, get_account_activity_user_ids

urlpatterns = [
    path('create-account-activity/', CreateAccountActivityNotificationView.as_view(), name='create-account-activity'),
    path('account-activity/', AccountActivityNotificationListView.as_view(), name='account-activity-list'),
    path('get-account-activity-user-ids/', get_account_activity_user_ids, name='get-account-activity-user-ids'),
]
