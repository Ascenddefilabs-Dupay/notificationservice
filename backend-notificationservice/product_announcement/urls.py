from django.urls import path
from .views import CreateProductAnnouncementNotificationView

urlpatterns = [
    path('create-product-announcement-notification/', CreateProductAnnouncementNotificationView.as_view(), name='create-product-announcement-notification'),
]
