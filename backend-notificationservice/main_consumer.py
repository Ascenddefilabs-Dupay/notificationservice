import os
import django
import pika
import json
import logging

# Set up Django settings before importing any Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from account_activity.models import AccountActivityNotifications
from insights_tips.models import InsightsTipsNotifications
from special_offers.models import SpecialOffersNotifications
from product_announcement.models import ProductAnnouncementNotifications
from PushNotification1.models import MessagesNotifications
from price_alerts.models import PriceAlertsNotifications

logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    try:
        # Decode the message
        message = json.loads(body.decode('utf-8'))
        user_id = message.get('user_id')
        content = message.get('content')

        if user_id and content:
            # Save the notification in the database
            if 'account_activity' in method.routing_key:
                notification = AccountActivityNotifications(user_id=user_id, content=content)
            elif 'insights_tips' in method.routing_key:
                notification = InsightsTipsNotifications(user_id=user_id, content=content)
            elif 'special_offers' in method.routing_key:
                notification = SpecialOffersNotifications(user_id=user_id, content=content)
            elif 'product_announcement' in method.routing_key:
                notification = ProductAnnouncementNotifications(user_id=user_id, content=content)
            elif 'messages' in method.routing_key:
                notification = MessagesNotifications(user_id=user_id, content=content)
            elif 'price_alerts' in method.routing_key:
                notification = PriceAlertsNotifications(user_id=user_id, content=content)
            else:
                logger.error("Invalid queue name received")
                return

            notification.save()
            logger.info(f"Notification saved for user {user_id}")
        else:
            logger.error("Invalid message format received")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to process message: {str(e)}")

def start_consuming():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        # connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Declare the queues
        channel.queue_declare(queue='account_activity_queue')
        channel.queue_declare(queue='insights_tips_queue')
        channel.queue_declare(queue='special_offers_queue')
        channel.queue_declare(queue='product_announcement_queue')
        channel.queue_declare(queue='messages_queue')
        channel.queue_declare(queue='price_alerts_queue')

        # Set up the consumers
        channel.basic_consume(queue='account_activity_queue', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='insights_tips_queue', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='special_offers_queue', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='product_announcement_queue', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='messages_queue', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='price_alerts_queue', on_message_callback=callback, auto_ack=True)

        logger.info('Waiting for messages. To exit, press CTRL+C')

        # Start consuming messages
        channel.start_consuming()

    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

if __name__ == "__main__":
    start_consuming()