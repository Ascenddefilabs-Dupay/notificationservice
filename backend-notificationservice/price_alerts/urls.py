from django.urls import path
from .views import (
    GetPriceAlertsUserIdsView,
    CreatePriceAlertsNotificationView,
    AdminManageCryptoCurrenciesListCreateView,
    AdminManageCryptoCurrenciesRetrieveUpdateDestroyView,
    GetLatestAdminPriceAlertsView,
)

urlpatterns = [
    path('get-price-alerts-user-ids/', GetPriceAlertsUserIdsView.as_view(), name='get-price-alerts-user-ids'),
    path('create-price-alerts/', CreatePriceAlertsNotificationView.as_view(), name='create-price-alerts'),
    path('admin-manage-crypto-currencies/', AdminManageCryptoCurrenciesListCreateView.as_view(), name='admin-manage-crypto-currencies-list-create'),
    path('admin-manage-crypto-currencies/<str:currency_id>/', AdminManageCryptoCurrenciesRetrieveUpdateDestroyView.as_view(), name='admin-manage-crypto-currencies-detail'),
    path('get-latest-admin-price-alerts/', GetLatestAdminPriceAlertsView.as_view(), name='get-latest-admin-price-alerts'),
]
