from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminSpecialOffers, SpecialOffersNotifications
import logging

logger = logging.getLogger(__name__)

class CreateSpecialOffersNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Fetch all user IDs where special_offers is True
            settings = NotificationSettings.objects.filter(special_offers=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with special offers enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Get the latest special offer content from AdminSpecialOffers table
            special_offer = AdminSpecialOffers.objects.latest('created_at')

            for user_id in user_ids:
                notification = SpecialOffersNotifications(
                    user_id=user_id,
                    content=special_offer.content
                )
                notification.save()

            return Response({
                "message": "Special offers notifications triggered successfully.",
                "special_offer_content": special_offer.content  # Return the special offer content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating special offers notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetSpecialOffersUserIds(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(special_offers=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                return Response({'error': 'No users with special offers enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user_ids for special offers: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
