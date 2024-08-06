from django.shortcuts import render
from rest_framework import viewsets
from .models import Notification
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.views import View
from django.http import HttpResponse
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer
import random
from django.conf import settings
from .models import Notification, TempOTP
from .serializers import TempOTPSerializer

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email_id')
        if not email:
            return Response({"error": "Email ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = random.randint(100000, 999999)

        # Format the email content
        subject = "OTP Verification"
        html_message = (
            f"Hi,<br><br>"
            "Welcome to Dupay.<br>"
            f"Please use the following One Time Password (OTP) to verify your email: <strong>{otp}</strong>.<br>"
            "Do not share this OTP with anyone.<br><br>"
            "Thank you!<br>"
            "The Dupay Team.<br>"
        )
        # plain_message = (
        #     "Hi,\n\n"
        #     "Welcome to Dupay.\n"
        #     f"Please use the following One Time Password (OTP) to verify your email: {otp}.\n"
        #     "Do not share this OTP with anyone.\n"
        #     "Thank you!\n"
        #     "The Dupay Team\n"
        # )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        # Send OTP email
        email_message = EmailMessage(subject, html_message, from_email, recipient_list)
        # email_message.attach_alternative(html_message, "text/html")
        email_message.content_subtype = "html"
        email_message.send(fail_silently=False)

        print(f"OTP for {email} is {otp}")

        # Save OTP to TempOTP model
        TempOTP.objects.create(email=email, otp=str(otp))

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.data.get('email_id')
        received_otp = request.data.get('otp')

        print("Received email:", email)
        print("Received OTP:", received_otp)

        try:
            temp_otp = TempOTP.objects.get(email=email, otp=received_otp)
            notification, created = Notification.objects.get_or_create(email_id=email)
            notification.verification_status = True
            notification.save()
            temp_otp.delete()  # Delete the temporary OTP entry after verification
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except TempOTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class VerifyEmailView(APIView):
#     def post(self, request):
#         email = request.data.get('email_id')
#         if not email:
#             return Response({"error": "Email ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         otp = random.randint(100000, 999999)

#         # Format the email content
#         subject = "OTP Verification"
#         message = (
#             "Hi,\n\n"
#             "Welcome to Dupay.\n"
#             f"Please use the following One Time Password (OTP) to verify your email: {otp}.\n"
#             "Do not share this OTP with anyone.\n\n"
#             "Thank you!\n"
#             "The Dupay Team\n"
#         )
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [email]

#         # Send OTP email
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         print(f"OTP for {email} is {otp}")

#         # Save OTP to TempOTP model
#         TempOTP.objects.create(email=email, otp=str(otp))

#         return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

#     def put(self, request):
#         email = request.data.get('email_id')
#         received_otp = request.data.get('otp')

#         print("Received email:", email)
#         print("Received OTP:", received_otp)

#         try:
#             temp_otp = TempOTP.objects.get(email=email, otp=received_otp)
#             notification, created = Notification.objects.get_or_create(email_id=email)
#             notification.verification_status = True
#             notification.save()
#             temp_otp.delete()  # Delete the temporary OTP entry after verification
#             return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
#         except TempOTP.DoesNotExist:
#             return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request):
#         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# from django.shortcuts import render
# from rest_framework import viewsets
# from .models import Notification
# from rest_framework.response import Response
# from django.utils.crypto import get_random_string
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.core.mail import send_mail
# from django.views import View
# from django.http import HttpResponse
# import json
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Notification
# from .serializers import NotificationSerializer
# import random
# from django.conf import settings
# from .models import Notification, TempOTP
# from .serializers import TempOTPSerializer

# class VerifyEmailView(APIView):
#     def post(self, request):
#         email = request.data.get('email_id')
#         if not email:
#             return Response({"error": "Email ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         otp = random.randint(100000, 999999)

#         # Send OTP
#         send_mail(
#             "OTP verfication",
#             "Hi,",
#             "Welcome to Dupay",
#             "   ",
#             f"Please use the following  One Time Password (OTP) to verify your Email: {otp}. Do not share this OTP with anyone.",
#             "Thank you!",
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
#         print(f"OTP for {email} is {otp}")

#         # Save OTP to TempOTP model
#         TempOTP.objects.create(email=email, otp=str(otp))

#         return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

#     def put(self, request):
#         email = request.data.get('email_id')
#         received_otp = request.data.get('otp')

#         print("Received email:", email)
#         print("Received OTP:", received_otp)

#         try:
#             temp_otp = TempOTP.objects.get(email=email, otp=received_otp)
#             notification, created = Notification.objects.get_or_create(email_id=email)
#             notification.verification_status = True
#             notification.save()
#             temp_otp.delete()  # Delete the temporary OTP entry after verification
#             return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
#         except TempOTP.DoesNotExist:
#             return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request):
#         return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
