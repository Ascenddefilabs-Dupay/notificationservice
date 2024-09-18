from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from account_activity.models import AccountActivityNotifications
from insights_tips.models import InsightsTipsNotifications
from product_announcement.models import ProductAnnouncementNotifications
from special_offers.models import SpecialOffersNotifications
from PushNotification1.models import MessagesNotifications
from price_alerts.models import PriceAlertsNotifications
from .models import Transaction
from datetime import datetime, timedelta

# Get today's and yesterday's dates
today = datetime.now().date()
yesterday = today - timedelta(days=1)

def fetch_notifications(request):
    user_id = request.GET.get('user_id', None)
    wallet_id = request.GET.get('wallet_id', None)  # Allow dynamic wallet_id input
    
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)
    
    if not wallet_id:
        return JsonResponse({'error': 'Wallet ID is required'}, status=400)

    # Time limit for non-transaction notifications
    three_days_ago = timezone.now() - timedelta(days=3)

    # Query all notification types except transactions (with 3-day limit)
    try:
        account_activity = AccountActivityNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
        insights_tips = InsightsTipsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
        product_announcements = ProductAnnouncementNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
        special_offers = SpecialOffersNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
        messages = MessagesNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
        price_alerts = PriceAlertsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)

        # Fetch transaction notifications without the 3-day limit
        transactions = Transaction.objects.filter(wallet_id=wallet_id)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching notifications: {str(e)}'}, status=500)

    # Combine all non-transaction notifications
    notifications = (
        list(account_activity) + 
        list(insights_tips) + 
        list(product_announcements) + 
        list(special_offers) + 
        list(messages) + 
        list(price_alerts)
    )

    # Convert non-transaction notifications into a dictionary format
    notifications_data = [
        {
            'content': str(notif.content),  # You can customize how the content should appear
            'created_at': (
            f"Today {notif.created_at.strftime('%H:%M:%S')}" if notif.created_at.date() == today 
            else f"Yesterday {notif.created_at.strftime('%H:%M:%S')}" if notif.created_at.date() == yesterday 
            else notif.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )
            # 'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for notif in notifications
    ]

    # Convert transactions into the same structure as notifications
    transaction_data = [
        {
            'content': (
                f"{trans.transaction_type} of {trans.transaction_currency} {format(trans.transaction_amount, '.2f')} on {trans.transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S')}. "
                f"Transaction Status is { 'Successful' if trans.transaction_status == 'Success' else 'Failed' if trans.transaction_status == 'failed' else 'Pending' }. "
                f"Sent by {trans.sender_mobile_number}. Received by {trans.user_phone_number}-Dupay"
            ),
            'created_at': (
            f"Today {trans.transaction_timestamp.strftime('%H:%M:%S')}" if trans.transaction_timestamp.date() == today 
            else f"Yesterday {trans.transaction_timestamp.strftime('%H:%M:%S')}" if trans.transaction_timestamp.date() == yesterday 
            else trans.transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )
        }
        for trans in transactions
    ]
    # transaction_data = [
    #     {
    #         'content': (
    #             f"{trans.transaction_type} of ₹{trans.transaction_amount} on {trans.transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S')}. "
    #             f"Transaction Status is  {trans.transaction_status}. Sent by {trans.sender_mobile_number}. Recived by {trans.user_phone_number}-Dupay"
    #         ),
    #         'created_at': trans.transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Use transaction_timestamp as created_at equivalent
    #     }
    #     for trans in transactions
    # ]

    # Combine all notifications and sort them by created_at
    all_notifications = notifications_data + transaction_data
    all_notifications.sort(key=lambda x: x['created_at'], reverse=True)

    return JsonResponse(all_notifications, safe=False)










# # notifications/views.py
# from django.http import JsonResponse
# from django.utils import timezone  # Import timezone utilities
# from datetime import timedelta  # Import timedelta for date calculations
# from account_activity.models import AccountActivityNotifications
# from insights_tips.models import InsightsTipsNotifications
# from product_announcement.models import ProductAnnouncementNotifications
# from special_offers.models import SpecialOffersNotifications
# from PushNotification1.models import MessagesNotifications
# from price_alerts.models import PriceAlertsNotifications

# def fetch_notifications(request):
#     # Get user_id from the request query parameters
#     user_id = request.GET.get('user_id', None)
    
#     if not user_id:
#         return JsonResponse({'error': 'User ID is required'}, status=400)

#     # Get the datetime for 3 days ago
#     three_days_ago = timezone.now() - timedelta(days=3)

#     # Fetch notifications from various models filtered by user_id and created_at (last 3 days)
#     account_activity = AccountActivityNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
#     insights_tips = InsightsTipsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
#     product_announcements = ProductAnnouncementNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
#     special_offers = SpecialOffersNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
#     messages = MessagesNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)
#     price_alerts = PriceAlertsNotifications.objects.filter(user_id=user_id, created_at__gte=three_days_ago)

#     # Combine all notifications
#     notifications = list(account_activity) + list(insights_tips) + list(product_announcements) + \
#                     list(special_offers) + list(messages) + list(price_alerts)

#     # Ensure all datetimes are timezone-aware for comparison
#     for notif in notifications:
#         if timezone.is_naive(notif.created_at):
#             notif.created_at = timezone.make_aware(notif.created_at)

#     # Sort by most recent
#     notifications.sort(key=lambda x: x.created_at, reverse=True)

#     # Prepare the response
#     notifications_data = [
#         {
#             'content': notif.content, 
#             'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#         }
#         for notif in notifications
#     ]

#     return JsonResponse(notifications_data, safe=False)
