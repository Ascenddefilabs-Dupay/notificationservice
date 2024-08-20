# special_offers/serializers.py
from rest_framework import serializers
from PushNotification1.models import NotificationSettings, EmailVerificationNotification

class SpecialOffersNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

class SpecialOffersSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'special_offers']  # Use the special_offers field
