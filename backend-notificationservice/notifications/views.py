# notifications/views.py
from django.http import JsonResponse
from django.utils import timezone  # Import timezone utilities
from datetime import timedelta  # Import timedelta for date calculations
from account_activity.models import AccountActivityNotifications
from insights_tips.models import InsightsTipsNotifications
from product_announcement.models import ProductAnnouncementNotifications
from special_offers.models import SpecialOffersNotifications
from PushNotification1.models import MessagesNotifications
from price_alerts.models import PriceAlertsNotifications

def fetch_notifications(request):
    # Get user_id from the request query parameters
    user_id = request.GET.get('user_id', None)
    
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    # Get the datetime for 3 days ago
    three_days_ago = timezone.now() - timedelta(days=3)

    # Fetch notifications from various models filtered by user_id and created_at (last 3 days)
    account_activity = AccountActivityNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
    insights_tips = InsightsTipsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
    product_announcements = ProductAnnouncementNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
    special_offers = SpecialOffersNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
    messages = MessagesNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
    price_alerts = PriceAlertsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)

    # Combine all notifications
    notifications = list(account_activity) + list(insights_tips) + list(product_announcements) + \
                    list(special_offers) + list(messages) + list(price_alerts)

    # Ensure all datetimes are timezone-aware for comparison
    for notif in notifications:
        if timezone.is_naive(notif.created_at):
            notif.created_at = timezone.make_aware(notif.created_at)

    # Sort by most recent
    notifications.sort(key=lambda x: x.created_at, reverse=True)

    # Prepare the response
    notifications_data = [
        {
            'content': notif.content, 
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for notif in notifications
    ]

    return JsonResponse(notifications_data, safe=False)
