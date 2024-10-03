# serializers.py
from rest_framework import serializers
from .models import SpecialOffersNotifications, AdminSpecialOffers

class SpecialOffersNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffersNotifications
        fields = '__all__'

class AdminSpecialOffersSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AdminSpecialOffers
        fields = ['content_id', 'content', 'created_at', 'updated_at']
