from rest_framework import serializers
from .models import MessagesNotifications, NotificationSettings

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'messages']

class MessagesNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesNotifications
        fields = '__all__'
