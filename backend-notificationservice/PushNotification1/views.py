import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import AdminMessages, MessagesNotifications, NotificationSettings
import logging
from .serializers import AdminMessagesSerializer

logger = logging.getLogger(__name__)

# Function to publish message to RabbitMQ
def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='messages_queue')

        # Publish message
        channel.basic_publish(exchange='', routing_key='messages_queue', body=message)

        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class CreateMessagesNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data.get('content_id')
            if not content_id:
                return Response({"error": "content_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                messages = AdminMessages.objects.get(content_id=content_id)
            except AdminMessages.DoesNotExist:
                return Response({"error": "AdminMessages with given content_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch all user IDs where messages is True
            settings = NotificationSettings.objects.filter(messages=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with messages enabled."}, status=status.HTTP_404_NOT_FOUND)

            # For each user, send a message to RabbitMQ
            for user_id in user_ids:
                notification_data = {
                    "user_id": user_id,
                    "content": messages.content
                }
                publish_to_rabbitmq(json.dumps(notification_data))

            return Response({
                "message": "Messages notifications queued successfully.",
                "messages_content": messages.content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetMessagesUserIds(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(messages=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                return Response({'error': 'No users with messages enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user_ids for messages: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminMessagesListCreateView(generics.ListCreateAPIView):
    queryset = AdminMessages.objects.all()
    serializer_class = AdminMessagesSerializer

class AdminMessagesUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminMessages.objects.all()
    serializer_class = AdminMessagesSerializer
    lookup_field = 'content_id'
