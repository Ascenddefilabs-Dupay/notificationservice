# import os
# import django
# import pika
# import json
# import logging

# # Set up Django settings before importing any Django models
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # Replace 'backend.settings' with the actual path to your settings module
# django.setup()

# from insights_tips.models import InsightsTipsNotifications

# logger = logging.getLogger(__name__)

# def callback(ch, method, properties, body):
#     try:
#         # Decode the message
#         message = json.loads(body.decode('utf-8'))
#         user_id = message.get('user_id')
#         content = message.get('content')

#         if user_id and content:
#             # Save the notification in the database
#             notification = InsightsTipsNotifications(user_id=user_id, content=content)
#             notification.save()
#             logger.info(f"Notification saved for user {user_id}")
#         else:
#             logger.error("Invalid message format received")
    
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decoding error: {str(e)}")
#     except Exception as e:
#         logger.error(f"Failed to process message: {str(e)}")


# def start_consuming():
#     try:
#         # Connect to RabbitMQ
#         connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#         channel = connection.channel()

#         # Declare the queue
#         channel.queue_declare(queue='insights_tips_queue')

#         # Set up the consumer
#         channel.basic_consume(queue='insights_tips_queue', on_message_callback=callback, auto_ack=True)

#         logger.info('Waiting for messages. To exit, press CTRL+C')

#         # Start consuming messages
#         channel.start_consuming()

#     except Exception as e:
#         logger.error(f"RabbitMQ Exception: {str(e)}")
#         raise e

# if __name__ == "__main__":
#     start_consuming()
