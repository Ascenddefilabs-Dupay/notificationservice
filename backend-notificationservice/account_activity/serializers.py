# serializers.py
from rest_framework import serializers
from .models import AccountActivityNotifications, AdminAccountActivity

class AccountActivityNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivityNotifications
        fields = '__all__'

class AdminAccountActivitySerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AdminAccountActivity
        fields = ['content_id', 'content', 'created_at', 'updated_at']
