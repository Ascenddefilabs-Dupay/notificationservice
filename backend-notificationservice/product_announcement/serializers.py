from rest_framework import serializers
from .models import ProductAnnouncementNotifications

class ProductAnnouncementNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnnouncementNotifications
        fields = '__all__'
