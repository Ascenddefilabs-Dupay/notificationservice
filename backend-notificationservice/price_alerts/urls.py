# price_alerts/urls.py
from django.urls import path
from .views import CreatePriceAlertsNotificationView, PriceAlertsNotificationListView, get_price_alerts_user_ids

urlpatterns = [
    path('create-price-alerts/', CreatePriceAlertsNotificationView.as_view(), name='create-price-alerts'),
    path('price-alerts/', PriceAlertsNotificationListView.as_view(), name='price-alerts-list'),
    path('get-price-alerts-user-ids/', get_price_alerts_user_ids, name='get-price-alerts-user-ids'),
]
