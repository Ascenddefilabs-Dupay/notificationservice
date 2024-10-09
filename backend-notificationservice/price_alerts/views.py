# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import requests
import json
import pika
from decimal import Decimal
from datetime import datetime, timedelta
from PushNotification1.models import NotificationSettings
from .models import AdminPriceAlerts, AdminManageCryptoCurrencies, PriceAlertsNotifications
from .serializers import PriceAlertsNotificationSerializer, AdminManageCryptoCurrenciesSerializer, AdminPriceAlertsSerializer
import logging

# Constants 
COINGECKO_API_URL_TEMPLATE = 'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr'

logger = logging.getLogger(__name__)

def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='price_alerts_queue')
        channel.basic_publish(exchange='', routing_key='price_alerts_queue', body=message)
        connection.close()
        logger.info("Message published to RabbitMQ: %s", message)  # Debugging
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

class AdminManageCryptoCurrenciesListCreateView(generics.ListCreateAPIView):
    queryset = AdminManageCryptoCurrencies.objects.all()
    serializer_class = AdminManageCryptoCurrenciesSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(f"Received POST data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class AdminManageCryptoCurrenciesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminManageCryptoCurrencies.objects.all()
    serializer_class = AdminManageCryptoCurrenciesSerializer
    lookup_field = 'currency_id'

    def update(self, request, *args, **kwargs):
        logger.debug(f"Received PUT data for {kwargs.get('currency_id')}: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)

class CreatePriceAlertsNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        logger.debug(f"Received POST data for create-price-alerts: {request.data}")
        try:
            # Fetch all user IDs where price alerts are enabled
            settings = NotificationSettings.objects.filter(price_alerts=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with price alerts enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Fetch all currencies from admin_manage_crypto_currencies
            currencies = AdminManageCryptoCurrencies.objects.all()
            if not currencies:
                return Response({"error": "No currencies configured for price alerts."}, status=status.HTTP_400_BAD_REQUEST)

            # Build CoinGecko API URL
            coin_ids = ','.join([currency.coin_gecko_id for currency in currencies])
            api_url = COINGECKO_API_URL_TEMPLATE.format(ids=coin_ids)

            # Fetch current prices
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Get current date
            today = datetime.now().date()
            notifications_content = []

            # Iterate over each currency
            for currency in currencies:
                current_price = Decimal(str(data.get(currency.coin_gecko_id, {}).get('inr', 0)))
                if current_price == 0:
                    continue  # Skip if price not found

                # Get opening price for the day
                try:
                    opening_alert = AdminPriceAlerts.objects.filter(
                        currency=currency,
                        created_at__date=today,
                        content__icontains='Opening price for the day'
                    ).latest('created_at')
                    opening_price = opening_alert.price_inr
                except AdminPriceAlerts.DoesNotExist:
                    # If no opening price, set current price as opening price
                    AdminPriceAlerts.objects.create(
                        content=f"{currency.coin_gecko_id} Opening price for the day",
                        currency=currency,
                        price_inr=current_price
                    )
                    opening_price = current_price

                # Calculate price change percentage
                if opening_price == 0:
                    continue  # Avoid division by zero
                price_change = ((current_price - opening_price) / opening_price) * 100

                # Check if price change exceeds the threshold
                if abs(price_change) >= currency.price_change_threshold:
                    direction = "increased" if price_change > 0 else "decreased"

                    # For each user, send notification
                    for user_id in user_ids:
                        notification_data = {
                            "user_id": user_id,
                            "content": f"{currency.symbol} price {direction} by {price_change:.2f}% (New Price: ₹{current_price})"
                        }
                        # Publish the message to RabbitMQ
                        publish_to_rabbitmq(json.dumps(notification_data))

                    # Add notification content for response
                    notifications_content.append(f"{currency.symbol} price {direction} by {price_change:.2f}%")

                    # Update the latest price in AdminPriceAlerts
                    AdminPriceAlerts.objects.create(
                        content=f"{currency.coin_gecko_id} Price {direction} by {price_change:.2f}% New Price: ₹{current_price}",
                        currency=currency,
                        price_inr=current_price
                    )

            if notifications_content:
                return Response({
                    "message": "Price Alerts notifications queued successfully.",
                    "price_alerts_content": notifications_content,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": "No price changes exceeded the thresholds.",
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Exception occurred while queuing notifications: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetPriceAlertsUserIdsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            settings = NotificationSettings.objects.filter(price_alerts=True)
            user_ids = [setting.user_id for setting in settings]

            if user_ids:
                return Response({'user_ids': user_ids})
            else:
                logger.info("No users with price alerts enabled.")  # Debugging
                return Response({'error': 'No users with price alerts enabled.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Exception occurred while fetching user IDs for price alerts: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetLatestAdminPriceAlertsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            today = datetime.now().date()
            five_days_ago = today - timedelta(days=5)
            alerts = AdminPriceAlerts.objects.filter(
                created_at__date__gte=five_days_ago
            ).order_by('-created_at')[:100]  # Limit to 100 for performance
            serializer = AdminPriceAlertsSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception occurred while fetching latest price alerts: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
