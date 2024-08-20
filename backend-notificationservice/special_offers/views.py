# special_offers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import EmailVerificationNotification, NotificationSettings
from .serializers import SpecialOffersNotificationSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class CreateSpecialOffersNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        email_id = request.data.get('email_id')
        message = request.data.get('message')
        notification_type = 'special_offers'

        logger.debug(f"Received email_id: {email_id}, message: {message}, type: {notification_type}")

        if not email_id or not message:
            return Response(
                {"error": "email_id and message fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch all user IDs where special_offers is True
            settings = NotificationSettings.objects.filter(special_offers=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with special offers enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Create and save notifications for each user
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

            serializer = SpecialOffersNotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating special offers notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpecialOffersNotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = EmailVerificationNotification.objects.filter(type='special_offers')
        serializer = SpecialOffersNotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_special_offers_user_ids(request):
    try:
        # Fetch all user_ids where special_offers is True
        settings = NotificationSettings.objects.filter(special_offers=True)
        user_ids = [setting.user_id for setting in settings]

        if user_ids:
            return JsonResponse({'user_ids': user_ids})
        else:
            return JsonResponse({'error': 'No users with special offers enabled found.'}, status=404)

    except Exception as e:
        logger.error(f"Exception occurred while fetching user_ids for special offers: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
