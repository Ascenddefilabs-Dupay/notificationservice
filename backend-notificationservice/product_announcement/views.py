from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import EmailVerificationNotification, NotificationSettings
from PushNotification1.serializers import NotificationSerializer
import logging

logger = logging.getLogger(__name__)

class CreateProductAnnouncementNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        email_id = request.data.get('email_id')
        message = request.data.get('message')
        notification_type = 'product_announcement'

        logger.debug(f"Received email_id: {email_id}, message: {message}, type: {notification_type}")

        if not email_id or not message:
            return Response(
                {"error": "email_id and message fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            settings = NotificationSettings.objects.filter(product_announcement=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with product announcement enabled."}, status=status.HTTP_404_NOT_FOUND)

            notifications = []
            for user_id in user_ids:
                notification = EmailVerificationNotification(
                    user_id=user_id,
                    email_id=email_id,
                    message=message,
                    type=notification_type,
                )
                notification.save()
                notifications.append(notification)

            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
