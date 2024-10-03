# views.py
import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminSpecialOffers, SpecialOffersNotifications
import logging
from .serializers import AdminSpecialOffersSerializer

logger = logging.getLogger(__name__)

# Function to publish message to RabbitMQ
def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='special_offers_queue')

        # Publish message
        channel.basic_publish(exchange='', routing_key='special_offers_queue', body=message)

        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class CreateSpecialOffersNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            content_id = request.data.get('content_id')
            if not content_id:
                return Response({"error": "content_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                special_offers = AdminSpecialOffers.objects.get(content_id=content_id)
            except AdminSpecialOffers.DoesNotExist:
                return Response({"error": "AdminSpecialOffers with given content_id does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch all user IDs where special offers is True
            settings = NotificationSettings.objects.filter(special_offers=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with special offers enabled."}, status=status.HTTP_404_NOT_FOUND)

            # For each user, send a message to RabbitMQ
            for user_id in user_ids:
                notification_data = {
                    "user_id": user_id,
                    "content": special_offers.content
                }
                publish_to_rabbitmq(json.dumps(notification_data))

            return Response({
                "message": "Special Offers notifications queued successfully.",
                "special_offers_content": special_offers.content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
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

class AdminSpecialOffersListCreateView(generics.ListCreateAPIView):
    queryset = AdminSpecialOffers.objects.all()
    serializer_class = AdminSpecialOffersSerializer

class AdminSpecialOffersUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminSpecialOffers.objects.all()
    serializer_class = AdminSpecialOffersSerializer
    lookup_field = 'content_id'
