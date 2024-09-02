from django.urls import path
from .views import GetSpecialOffersUserIds, CreateSpecialOffersNotificationView

urlpatterns = [
    path('get-special-offers-user-ids/', GetSpecialOffersUserIds.as_view(), name='get-special-offers-user-ids'),
    path('create-special-offers/', CreateSpecialOffersNotificationView.as_view(), name='create-special-offers'),
]
