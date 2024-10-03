# urls.py
from django.urls import path
from .views import (
    GetProductAnnouncementUserIds,
    CreateProductAnnouncementNotificationView,
    AdminProductAnnouncementListCreateView,
    AdminProductAnnouncementUpdateDeleteView,
)

urlpatterns = [
    path('get-product-announcement-user-ids/', GetProductAnnouncementUserIds.as_view(), name='get-product-announcement-user-ids'),
    path('create-product-announcement/', CreateProductAnnouncementNotificationView.as_view(), name='create-product-announcement-notification'),
    path('admin-product-announcement/', AdminProductAnnouncementListCreateView.as_view(), name='admin-product-announcement-list-create'),
    path('admin-product-announcement/<str:content_id>/', AdminProductAnnouncementUpdateDeleteView.as_view(), name='admin-product-announcement-update-delete'),
]
