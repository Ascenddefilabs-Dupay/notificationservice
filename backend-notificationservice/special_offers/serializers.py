from rest_framework import serializers
from .models import SpecialOffersNotifications

class SpecialOffersNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffersNotifications
        fields = '__all__'
