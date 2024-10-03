# serializers.py
from rest_framework import serializers
from .models import ProductAnnouncementNotifications, AdminProductAnnouncement

class ProductAnnouncementNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnnouncementNotifications
        fields = '__all__'

class AdminProductAnnouncementSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AdminProductAnnouncement
        fields = ['content_id', 'content', 'created_at', 'updated_at']
