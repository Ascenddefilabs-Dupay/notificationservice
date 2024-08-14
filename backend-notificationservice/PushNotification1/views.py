from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationNotification, NotificationSettings
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class CreateNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = str(request.data.get('user_id', '')).strip()
        email_id = request.data.get('email_id')
        message = request.data.get('message')
        notification_type = request.data.get('type')

        logger.debug(f"Received user_id: {user_id}, email_id: {email_id}, message: {message}, type: {notification_type}")

        if not user_id or not email_id or not message or not notification_type:
            return Response(
                {"error": "user_id, email_id, message, and type fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            settings = NotificationSettings.objects.get(user_id=user_id)
            notification = EmailVerificationNotification(
                user_id=user_id,
                email_id=email_id,
                message=message,
                type=notification_type,
            )
            notification.save()

            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except NotificationSettings.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Exception occurred while creating notification: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = EmailVerificationNotification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def get_user_id(request):
#     # Fetch user_id based on your actual logic
#     user_id = 'dupA0002'  # Placeholder logic
#     return JsonResponse({'user_id': user_id})
@api_view(['GET'])
def get_user_id(request):
    try:
        # Fetch the first user_id where messages is True
        settings = NotificationSettings.objects.filter(messages=True).first()

        if settings:
            return JsonResponse({'user_id': settings.user_id})
        else:
            return JsonResponse({'error': 'No user with messages enabled found.'}, status=404)

    except Exception as e:
        # Log the error and return a server error response
        logger.error(f"Exception occurred while fetching user_id: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import EmailVerificationNotification
# from .serializers import NotificationSerializer

# class CreateNotificationView(APIView):
#     def post(self, request, *args, **kwargs):
#         user_id = request.data.get('user_id')
#         email_id = request.data.get('email_id')
#         message = request.data.get('message')
#         notification_type = request.data.get('type')

#         if not user_id or not email_id or not message or not notification_type:
#             return Response(
#                 {"error": "user_id, email_id, message, and type fields are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             notification = EmailVerificationNotification(
#                 user_id=user_id,
#                 email_id=email_id,
#                 message=message,
#                 type=notification_type,
#             )
#             notification.save()

#             serializer = NotificationSerializer(notification)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class NotificationListView(APIView):
#     def get(self, request, *args, **kwargs):
#         notifications = EmailVerificationNotification.objects.all()
#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
