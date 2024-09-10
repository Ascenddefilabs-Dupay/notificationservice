from rest_framework import serializers
from .models import PriceAlertsNotifications

class PriceAlertsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlertsNotifications
        fields = '__all__'
