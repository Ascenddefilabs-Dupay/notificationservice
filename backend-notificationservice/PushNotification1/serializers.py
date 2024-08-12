from rest_framework import serializers
from .models import EmailVerificationNotification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationNotification
        fields = '__all__'  # This will include all fields in the model


# from rest_framework import serializers
# from .models import EmailVerificationNotification

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmailVerificationNotification
#         fields = '__all__'