from rest_framework import serializers
from .models import Notification
from .models import TempOTP


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class TempOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempOTP
        fields = ['email', 'otp', 'created_at']