# special_offers/urls.py
from django.urls import path
from .views import CreateSpecialOffersNotificationView, SpecialOffersNotificationListView, get_special_offers_user_ids

urlpatterns = [
    path('create-special-offers/', CreateSpecialOffersNotificationView.as_view(), name='create-special-offers'),
    path('special-offers/', SpecialOffersNotificationListView.as_view(), name='special-offers-list'),
    path('get-special-offers-user-ids/', get_special_offers_user_ids, name='get-special-offers-user-ids'),
]
