from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminInsightsTips, InsightsTipsNotifications
import logging

logger = logging.getLogger(__name__)

class CreateInsightsTipsNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Fetch all user IDs where insights tips is True
            settings = NotificationSettings.objects.filter(insights_tips=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with insights tips enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Get the latest insights tips content from AdminInsightsTips table
            insights_tips = AdminInsightsTips.objects.latest('created_at')

            for user_id in user_ids:
                notification = InsightsTipsNotifications(
                    user_id=user_id,
                    content=insights_tips.content
                )
                notification.save()

            return Response({
                "message": "Insights Tips notifications triggered successfully.",
                "insights_tips_content": insights_tips.content  # Return the insights tips content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating insights tips notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetInsightsTipsUserIds(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(insights_tips=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                return Response({'error': 'No users with insights tips enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user_ids for insights tips: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
