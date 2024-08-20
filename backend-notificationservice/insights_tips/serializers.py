from rest_framework import serializers
from PushNotification1.models import NotificationSettings, EmailVerificationNotification

class InsightsTipsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

class InsightsTipsNotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'insights_tips']
