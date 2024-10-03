# serializers.py
from rest_framework import serializers
from .models import InsightsTipsNotifications, AdminInsightsTips

class InsightsTipsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsightsTipsNotifications
        fields = '__all__'

class AdminInsightsTipsSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AdminInsightsTips
        fields = ['content_id', 'content', 'created_at', 'updated_at']
