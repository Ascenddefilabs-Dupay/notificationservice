from rest_framework import serializers
from PushNotification1.models import EmailVerificationNotification, NotificationSettings

class ProductAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'

class ProductAnnouncementSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['user_id', 'product_announcement']
