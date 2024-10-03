# urls.py
from django.urls import path
from .views import (
    GetInsightsTipsUserIds,
    CreateInsightsTipsNotificationView,
    AdminInsightsTipsListCreateView,
    AdminInsightsTipsUpdateDeleteView,
)

urlpatterns = [
    path('get-insights-tips-user-ids/', GetInsightsTipsUserIds.as_view(), name='get-insights-tips-user-ids'),
    path('create-insights-tips/', CreateInsightsTipsNotificationView.as_view(), name='create-insights-tips-notification'),
    path('admin-insights-tips/', AdminInsightsTipsListCreateView.as_view(), name='admin-insights-tips-list-create'),
    path('admin-insights-tips/<str:content_id>/', AdminInsightsTipsUpdateDeleteView.as_view(), name='admin-insights-tips-update-delete'),
]
