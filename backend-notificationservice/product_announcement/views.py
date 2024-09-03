from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminProductAnnouncement, ProductAnnouncementNotifications
import logging

logger = logging.getLogger(__name__)

class CreateProductAnnouncementNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Fetch all user IDs where product announcement is True
            settings = NotificationSettings.objects.filter(product_announcement=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with product announcement enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Get the latest product announcement content from AdminProductAnnouncement table
            product_announcement = AdminProductAnnouncement.objects.latest('created_at')

            for user_id in user_ids:
                notification = ProductAnnouncementNotifications(
                    user_id=user_id,
                    content=product_announcement.content
                )
                notification.save()

            return Response({
                "message": "Product Announcement notifications triggered successfully.",
                "product_announcement_content": product_announcement.content  # Return the product announcement content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating product announcement notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetProductAnnouncementUserIds(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(product_announcement=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                return Response({'error': 'No users with product announcement enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user_ids for product announcement: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
