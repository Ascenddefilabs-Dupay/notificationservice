from rest_framework import serializers
from .models import AccountActivityNotifications

class AccountActivityNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivityNotifications
        fields = '__all__'
