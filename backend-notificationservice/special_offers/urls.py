# urls.py
from django.urls import path
from .views import (
    GetSpecialOffersUserIds,
    CreateSpecialOffersNotificationView,
    AdminSpecialOffersListCreateView,
    AdminSpecialOffersUpdateDeleteView,
)

urlpatterns = [
    path('get-special-offers-user-ids/', GetSpecialOffersUserIds.as_view(), name='get-special-offers-user-ids'),
    path('create-special-offers/', CreateSpecialOffersNotificationView.as_view(), name='create-special-offers-notification'),
    path('admin-special-offers/', AdminSpecialOffersListCreateView.as_view(), name='admin-special-offers-list-create'),
    path('admin-special-offers/<str:content_id>/', AdminSpecialOffersUpdateDeleteView.as_view(), name='admin-special-offers-update-delete'),
]
