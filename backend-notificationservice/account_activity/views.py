import pika
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import NotificationSettings
from .models import AdminAccountActivity, AccountActivityNotifications
import logging

logger = logging.getLogger(__name__)

# Function to publish message to RabbitMQ
def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue='account_activity_queue')

        # Publish message
        channel.basic_publish(exchange='', routing_key='account_activity_queue', body=message)

        connection.close()
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class CreateAccountActivityNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Fetch all user IDs where account activity is True
            settings = NotificationSettings.objects.filter(account_activity=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with account activity enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Get the latest account activity content from AdminAccountActivity table
            account_activity = AdminAccountActivity.objects.latest('created_at')

            # For each user, send a message to RabbitMQ
            for user_id in user_ids:
                notification_data = {
                    "user_id": user_id,
                    "content": account_activity.content
                }
                publish_to_rabbitmq(json.dumps(notification_data))

            return Response({
                "message": "Account Activity notifications queued successfully.",
                "account_activity_content": account_activity.content
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetAccountActivityUserIds(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(account_activity=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                return Response({'error': 'No users with account activity enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user_ids for account activity: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
