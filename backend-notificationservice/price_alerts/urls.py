# urls.py
from django.urls import path
from .views import (
    AdminManageCryptoCurrenciesListCreateView,
    AdminManageCryptoCurrenciesRetrieveUpdateDestroyView,
    CreatePriceAlertsNotificationView,
    GetPriceAlertsUserIdsView,
    GetLatestAdminPriceAlertsView
)

urlpatterns = [
    path('admin-manage-crypto-currencies/', AdminManageCryptoCurrenciesListCreateView.as_view(), name='admin-manage-crypto-currencies-list-create'),
    path('admin-manage-crypto-currencies/<str:currency_id>/', AdminManageCryptoCurrenciesRetrieveUpdateDestroyView.as_view(), name='admin-manage-crypto-currencies-retrieve-update-destroy'),
    path('create-price-alerts/', CreatePriceAlertsNotificationView.as_view(), name='create-price-alerts'),
    path('get-price-alerts-user-ids/', GetPriceAlertsUserIdsView.as_view(), name='get-price-alerts-user-ids'),
    path('get-latest-admin-price-alerts/', GetLatestAdminPriceAlertsView.as_view(), name='get-latest-admin-price-alerts'),
]
