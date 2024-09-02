from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from PushNotification1.models import EmailVerificationNotification, NotificationSettings

def notification_list(request):
    user_id = request.user.id  # Assuming user is authenticated
    notifications = EmailVerificationNotification.objects.filter(user_id=user_id).order_by('-created_at')
    notification_data = [{
        'notification_id': n.notification_id,
        'message': n.message,
        'status': n.status,
        'created_at': n.created_at,
    } for n in notifications]
    
    return JsonResponse({'notifications': notification_data})

def unread_notification_count(request):
    user_id = request.user.id
    unread_count = EmailVerificationNotification.objects.filter(user_id=user_id, status=False).count()
    return JsonResponse({'unread_count': unread_count})

@require_POST
def mark_as_read(request, notification_id):
    user_id = request.user.id
    notification = get_object_or_404(EmailVerificationNotification, notification_id=notification_id, user_id=user_id)
    
    if not notification.status:
        notification.status = True
        notification.save()
    
    return JsonResponse({'success': True})
