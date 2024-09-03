from django.urls import path
from .views import GetInsightsTipsUserIds, CreateInsightsTipsNotificationView

urlpatterns = [
    path('get-insights-tips-user-ids/', GetInsightsTipsUserIds.as_view(), name='get-insights-tips-user-ids'),
    path('create-insights-tips/', CreateInsightsTipsNotificationView.as_view(), name='create-insights-tips'),
]
