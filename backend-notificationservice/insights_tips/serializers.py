from rest_framework import serializers
from .models import InsightsTipsNotifications

class InsightsTipsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsightsTipsNotifications
        fields = '__all__'
