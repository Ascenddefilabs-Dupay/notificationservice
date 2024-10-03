# views.py
import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminProductAnnouncement, ProductAnnouncementNotifications
import logging
from .serializers import AdminProductAnnouncementSerializer

logger = logging.getLogger(__name__)

# Function to publish message to RabbitMQ
def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='product_announcement_queue')

        # Publish message
        channel.basic_publish(exchange='', routing_key='product_announcement_queue', body=message)

        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class CreateProductAnnouncementNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data.get('content_id')
            if not content_id:
                return Response({"error": "content_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product_announcement = AdminProductAnnouncement.objects.get(content_id=content_id)
            except AdminProductAnnouncement.DoesNotExist:
                return Response({"error": "AdminProductAnnouncement with given content_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch all user IDs where product announcement is True
            settings = NotificationSettings.objects.filter(product_announcement=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with product announcement enabled."}, status=status.HTTP_404_NOT_FOUND)

            # For each user, send a message to RabbitMQ
            for user_id in user_ids:
                notification_data = {
                    "user_id": user_id,
                    "content": product_announcement.content
                }
                publish_to_rabbitmq(json.dumps(notification_data))

            return Response({
                "message": "Product Announcement notifications queued successfully.",
                "product_announcement_content": product_announcement.content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
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

class AdminProductAnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = AdminProductAnnouncement.objects.all()
    serializer_class = AdminProductAnnouncementSerializer

class AdminProductAnnouncementUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminProductAnnouncement.objects.all()
    serializer_class = AdminProductAnnouncementSerializer
    lookup_field = 'content_id'
