from django.urls import path
from .views import GetPriceAlertsUserIds, CreatePriceAlertsNotificationView

urlpatterns = [
    path('get-price-alerts-user-ids/', GetPriceAlertsUserIds.as_view(), name='get-price-alerts-user-ids'),
    path('create-price-alerts/', CreatePriceAlertsNotificationView.as_view(), name='create-price-alerts'),
]
