# PushNotification/views.py
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import Notification, FCMToken
from firebase_admin import messaging, credentials
import json
import os
import firebase_admin
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred = credentials.Certificate(os.path.join(BASE_DIR, 'secrets', 'firebase-adminsdk.json'))
firebase_admin.initialize_app(cred)
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class SaveTokenView(View):
    def post(self, request, *args, **kwargs):
        try:
            logger.info('SaveTokenView POST request received')
            body = json.loads(request.body.decode('utf-8'))
            logger.info(f'Received body: {body}')
            token = body.get('token')
            if token:
                Notification.objects.update_or_create(user_token=token)
                logger.info('Token saved successfully')
                return JsonResponse({'message': 'Token saved'}, status=200)
            logger.warning('No token provided')
            return JsonResponse({'message': 'No token provided'}, status=400)
        except json.JSONDecodeError:
            logger.error('Invalid JSON')
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class SendNotificationView(View):
    def post(self, request, *args, **kwargs):
        try:
            logger.info('SendNotificationView POST request received')
            body = json.loads(request.body.decode('utf-8'))
            logger.info(f'Received body: {body}')
            token = body.get('token')
            title = body.get('title')
            body_text = body.get('body')

            if not token or not title or not body_text:
                logger.warning('Missing token, title, or body')
                return JsonResponse({'message': 'Missing token, title, or body'}, status=400)

            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body_text),
                token=token,
                webpush=messaging.WebpushConfig(
                    notification=messaging.WebpushNotification(
                        title=title,
                        body=body_text,
                        actions=[
                            {"action": "approve", "title": "Approve"},
                            {"action": "decline", "title": "Decline"}
                        ]
                    )
                )
            )

            response = messaging.send(message)
            logger.info('Notification sent successfully')
            return JsonResponse({'message': 'Notification sent', 'response': response}, status=200)
        except json.JSONDecodeError:
            logger.error('Invalid JSON')
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Error: {str(e)}')
            return JsonResponse({'message': str(e)}, status=500)
        
@csrf_exempt
def save_token(request):
    print(request)
    if request.method == 'GET':
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# @csrf_exempt
# def save_token(request):
#     logger.info(f'Request method: {request.method}')
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body.decode('utf-8'))
#             logger.info(f'Received body: {body}')
#             token = body.get('token')
#             if token:
#                 FCMToken.objects.create(token=token)
#                 logger.info('Token saved successfully')
#                 return JsonResponse({'status': 'success'})
#             else:
#                 logger.warning('No token provided')
#                 return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=400)
#         except json.JSONDecodeError:
#             logger.error('Invalid JSON')
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             logger.error(f'Error: {str(e)}')
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#     else:
#         logger.warning(f'Invalid request method: {request.method}')
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# @csrf_exempt
# def save_token(request):
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body.decode('utf-8'))
#             logger.debug(f'Received body: {body}')
#             token = body.get('token')
#             if token:
#                 FCMToken.objects.create(token=token)
#                 return JsonResponse({'status': 'success'})
#             else:
#                 logger.warning('No token provided')
#                 return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=400)
#         except json.JSONDecodeError:
#             logger.error('Invalid JSON')
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             logger.error(f'Error saving token: {str(e)}')
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#     logger.warning('Invalid request method')
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# @csrf_exempt
# def save_token(request):
    
#     if request.method == 'POST':
#         try:
#             print(request)
#             body = json.loads(request.body.decode('utf-8'))
#             print(body)
#             logger.debug(f'Received body: {body}')
#             print(logger)
#             token = body.get('token')
#             if token:
#                 FCMToken.objects.create(token=token)
#                 return JsonResponse({'status': 'success'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'No token provided'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



# # PushNotification/views.py
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from django.views import View
# from .models import Notification
# from firebase_admin import messaging, initialize_app, credentials
# import json
# import os
# import firebase_admin
# from firebase_admin import credentials

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# cred = credentials.Certificate(os.path.join(BASE_DIR, 'secrets', 'firebase-adminsdk.json'))
# firebase_admin.initialize_app(cred)

# @method_decorator(csrf_exempt, name='dispatch')
# class SaveTokenView(View):
#     def post(self, request, *args, **kwargs):
#         body = json.loads(request.body.decode('utf-8'))
#         token = body.get('token')
#         if token:
#             Notification.objects.update_or_create(user_token=token)
#             return JsonResponse({'message': 'Token saved'})
#         return JsonResponse({'message': 'No token provided'}, status=400)

# @method_decorator(csrf_exempt, name='dispatch')
# class SendNotificationView(View):
#     def post(self, request, *args, **kwargs):
#         body = json.loads(request.body.decode('utf-8'))
#         token = body.get('token')
#         title = body.get('title')
#         body_text = body.get('body')

#         message = messaging.Message(
#             notification=messaging.Notification(title=title, body=body_text),
#             token=token,
#             webpush=messaging.WebpushConfig(
#                 notification=messaging.WebpushNotification(
#                     title=title,
#                     body=body_text,
#                     actions=[
#                         {
#                             "action": "approve",
#                             "title": "Approve"
#                         },
#                         {
#                             "action": "decline",
#                             "title": "Decline"
#                         }
#                     ]
#                 )
#             )
#         )

#         response = messaging.send(message)
#         return JsonResponse({'message': 'Notification sent', 'response': response})
