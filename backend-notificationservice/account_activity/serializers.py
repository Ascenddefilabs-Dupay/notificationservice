# account_activity/serializers.py
from rest_framework import serializers
from PushNotification1.models import NotificationSettings, EmailVerificationNotification

class AccountActivityNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

class AccountActivitySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'account_activity']  # Use the account_activity field
