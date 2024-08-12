from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationNotification
from .serializers import NotificationSerializer

class CreateNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        email_id = request.data.get('email_id')
        message = request.data.get('message')
        notification_type = request.data.get('type')

        if not user_id or not email_id or not message or not notification_type:
            return Response(
                {"error": "user_id, email_id, message, and type fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            notification = EmailVerificationNotification(
                user_id=user_id,
                email_id=email_id,
                message=message,
                type=notification_type,
            )
            notification.save()

            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NotificationListView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = EmailVerificationNotification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from .models import EmailVerificationNotification
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import NotificationSerializer

# class CreateNotificationView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         message = request.data.get('message')

#         notification = EmailVerificationNotification(email=email, message=message)
#         notification.save()

#         return Response({
#             'notification_id': notification.notification_id,
#             'message': notification.message,
#         }, status=status.HTTP_201_CREATED)

# class NotificationListView(APIView):
#     def get(self, request):
#         notifications = EmailVerificationNotification.objects.all()
#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data)
