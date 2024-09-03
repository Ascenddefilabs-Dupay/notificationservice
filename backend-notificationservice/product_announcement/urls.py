from django.urls import path
from .views import GetProductAnnouncementUserIds, CreateProductAnnouncementNotificationView

urlpatterns = [
    path('get-product-announcement-user-ids/', GetProductAnnouncementUserIds.as_view(), name='get-product-announcement-user-ids'),
    path('create-product-announcement/', CreateProductAnnouncementNotificationView.as_view(), name='create-product-announcement'),
]
