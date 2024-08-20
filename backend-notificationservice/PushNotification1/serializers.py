
from rest_framework import serializers
from .models import EmailVerificationNotification, NotificationSettings

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'messages']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

