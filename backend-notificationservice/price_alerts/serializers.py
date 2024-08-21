# price_alerts/serializers.py
from rest_framework import serializers
from PushNotification1.models import NotificationSettings, EmailVerificationNotification

class PriceAlertsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

class PriceAlertsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'price_alerts']  # Use the price_alerts field
