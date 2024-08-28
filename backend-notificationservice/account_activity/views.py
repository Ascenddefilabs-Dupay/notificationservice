# account_activity/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PushNotification1.models import EmailVerificationNotification, NotificationSettings
from .serializers import AccountActivityNotificationSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import connection  # Added for raw SQL queries
import logging
import time

logger = logging.getLogger(__name__)

# Function to fetch the delay from the notification_timings table
def get_delay_from_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT account_activity_timing FROM notification_timings LIMIT 1;")
        row = cursor.fetchone()
    return row[0] if row else 10  # Default to 10 seconds if not found

# Function to create notifications with or without a delay
def create_notification(email_id, message, immediate=False):
    delay = 0 if immediate else get_delay_from_db()  # Set delay to 0 for immediate notifications
    logger.info(f"Notification will be sent after {delay} seconds delay.")
    time.sleep(delay)  # Introduce delay
    logger.info("Delay over, creating notification now.")
    
    try:
        settings = NotificationSettings.objects.filter(account_activity=True)
        user_ids = [setting.user_id for setting in settings]

        if not user_ids:
            logger.warning("No users with account activity enabled.")
            return None

        notifications = []
        for user_id in user_ids:
            notification = EmailVerificationNotification(
                user_id=user_id,
                email_id=email_id,
                message=message,
                type='account_activity',
            )
            try:
                notification.save()
                logger.info(f"Notification saved for user_id: {user_id}")
                notifications.append(notification)
            except Exception as e:
                logger.error(f"Failed to save notification for user_id: {user_id}, error: {str(e)}")

        return notifications

    except Exception as e:
        logger.error(f"Exception occurred while creating notifications: {str(e)}")
        return None

class CreateAccountActivityNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        email_id = request.data.get('email_id')
        message = request.data.get('message')
        immediate = request.data.get('immediate', False)  # Get the immediate flag from the request

        try:
            logger.debug(f"Received email_id: {email_id}, message: {message}, immediate: {immediate}")

            if not email_id or not message:
                return Response(
                    {"error": "email_id and message fields are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the notification with or without delay based on the immediate flag
            notifications = create_notification(email_id, message, immediate=immediate)

            if notifications is None:
                return Response(
                    {"error": "No users with account activity enabled or notification creation failed."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            serializer = AccountActivityNotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Exception occurred while creating account activity notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AccountActivityNotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = EmailVerificationNotification.objects.filter(type='account_activity')
        serializer = AccountActivityNotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_account_activity_user_ids(request):
    try:
        settings = NotificationSettings.objects.filter(account_activity=True)
        user_ids = [setting.user_id for setting in settings]

        if user_ids:
            return JsonResponse({'user_ids': user_ids})
        else:
            return JsonResponse({'error': 'No users with account activity enabled found.'}, status=404)

    except Exception as e:
        logger.error(f"Exception occurred while fetching user_ids for account activity: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)








# # account_activity/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from PushNotification1.models import EmailVerificationNotification, NotificationSettings
# from .serializers import AccountActivityNotificationSerializer
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# import logging

# logger = logging.getLogger(__name__)

# class CreateAccountActivityNotificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         email_id = request.data.get('email_id')
#         message = request.data.get('message')
#         notification_type = 'account_activity'

#         logger.debug(f"Received email_id: {email_id}, message: {message}, type: {notification_type}")

#         if not email_id or not message:
#             return Response(
#                 {"error": "email_id and message fields are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             # Fetch all user IDs where account_activity is True
#             settings = NotificationSettings.objects.filter(account_activity=True)
#             user_ids = [setting.user_id for setting in settings]

#             if not user_ids:
#                 return Response({"error": "No users with account activity enabled."}, status=status.HTTP_404_NOT_FOUND)

#             # Create and save notifications for each user
#             notifications = []
#             for user_id in user_ids:
#                 notification = EmailVerificationNotification(
#                     user_id=user_id,
#                     email_id=email_id,
#                     message=message,
#                     type=notification_type,
#                 )
#                 notification.save()
#                 notifications.append(notification)

#             serializer = AccountActivityNotificationSerializer(notifications, many=True)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             logger.error(f"Exception occurred while creating account activity notifications: {str(e)}")
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class AccountActivityNotificationListView(APIView):
#     def get(self, request, *args, **kwargs):
#         notifications = EmailVerificationNotification.objects.filter(type='account_activity')
#         serializer = AccountActivityNotificationSerializer(notifications, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def get_account_activity_user_ids(request):
#     try:
#         # Fetch all user_ids where account_activity is True
#         settings = NotificationSettings.objects.filter(account_activity=True)
#         user_ids = [setting.user_id for setting in settings]

#         if user_ids:
#             return JsonResponse({'user_ids': user_ids})
#         else:
#             return JsonResponse({'error': 'No users with account activity enabled found.'}, status=404)

#     except Exception as e:
#         logger.error(f"Exception occurred while fetching user_ids for account activity: {str(e)}")
#         return JsonResponse({'error': 'Internal server error'}, status=500)
