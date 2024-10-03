from rest_framework import serializers
from .models import MessagesNotifications, NotificationSettings, AdminMessages

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'messages']

class MessagesNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesNotifications
        fields = '__all__'

class AdminMessagesSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = AdminMessages
        fields = ['content_id', 'content', 'created_at', 'updated_at']
