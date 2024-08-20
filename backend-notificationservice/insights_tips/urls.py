from django.urls import path
from .views import CreateInsightsTipsNotificationView, InsightsTipsNotificationListView, get_insights_tips_user_ids

urlpatterns = [
    path('create-insights-tips-notification/', CreateInsightsTipsNotificationView.as_view(), name='create-insights-tips-notification'),
    path('insights-tips-notifications/', InsightsTipsNotificationListView.as_view(), name='insights-tips-notification-list'),
    path('get_insights_tips_user_ids/', get_insights_tips_user_ids, name='get_insights_tips_user_ids'),
]
