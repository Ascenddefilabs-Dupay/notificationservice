# views.py
import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminInsightsTips, InsightsTipsNotifications
import logging
from .serializers import AdminInsightsTipsSerializer

logger = logging.getLogger(__name__)

# Function to publish message to RabbitMQ
def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='insights_tips_queue')

        # Publish message
        channel.basic_publish(exchange='', routing_key='insights_tips_queue', body=message)

        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class CreateInsightsTipsNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data.get('content_id')
            if not content_id:
                return Response({"error": "content_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                insights_tips = AdminInsightsTips.objects.get(content_id=content_id)
            except AdminInsightsTips.DoesNotExist:
                return Response({"error": "AdminInsightsTips with given content_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch all user IDs where insights tips is True
            settings = NotificationSettings.objects.filter(insights_tips=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with insights tips enabled."}, status=status.HTTP_404_NOT_FOUND)

            # For each user, send a message to RabbitMQ
            for user_id in user_ids:
                notification_data = {
                    "user_id": user_id,
                    "content": insights_tips.content
                }
                publish_to_rabbitmq(json.dumps(notification_data))

            return Response({
                "message": "Insights Tips notifications queued successfully.",
                "insights_tips_content": insights_tips.content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
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

class AdminInsightsTipsListCreateView(generics.ListCreateAPIView):
    queryset = AdminInsightsTips.objects.all()
    serializer_class = AdminInsightsTipsSerializer

class AdminInsightsTipsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminInsightsTips.objects.all()
    serializer_class = AdminInsightsTipsSerializer
    lookup_field = 'content_id'
