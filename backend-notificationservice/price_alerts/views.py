from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import pika
from decimal import Decimal
from datetime import datetime, timedelta
from PushNotification1.models import NotificationSettings
from .models import AdminPriceAlerts
import logging

# Constants
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=inr'
PRICE_CHANGE_THRESHOLD = 0.30  # 5% price change threshold

logger = logging.getLogger(__name__)

def publish_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='price_alerts_queue')
        channel.basic_publish(exchange='', routing_key='price_alerts_queue', body=message)
        connection.close()
        print("Message published to RabbitMQ:", message)  # Debugging
    except Exception as e:
        logger.error(f"RabbitMQ Exception: {str(e)}")
        raise e

def fetch_current_price():
    try:
        response = requests.get(COINGECKO_API_URL)
        response.raise_for_status()
        data = response.json()
        price = Decimal(data['ethereum']['inr'])
        print(f"Fetched new price from API: ₹{price}")  # Debugging
        return price
    except Exception as e:
        logger.error(f"Error fetching price from CoinGecko: {str(e)}")
        raise e

# Function to calculate the percentage price change from the opening price
def calculate_change(opening_price, current_price):
    try:
        change = ((current_price - opening_price) / opening_price) * 100
        print(f"Opening Price: {opening_price}, Current Price: {current_price}, Change: {change}")  # Debugging
        return change
    except ZeroDivisionError as e:
        logger.error(f"Error calculating price change: {str(e)}")
        raise e

class CreatePriceAlertsNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Fetch all user IDs where price alerts are enabled
            settings = NotificationSettings.objects.filter(price_alerts=True)
            user_ids = [setting.user_id for setting in settings]

            if not user_ids:
                return Response({"error": "No users with price alerts enabled."}, status=status.HTTP_404_NOT_FOUND)

            # Fetch the current price from CoinGecko
            new_price = fetch_current_price()
            print(f"Fetched new price: {new_price}")  # Debugging

            # Get the current date
            today = datetime.now().date()

            try:
                # Get the opening price for the day
                price_alerts = AdminPriceAlerts.objects.latest('created_at')
                old_price = price_alerts.price_inr
                price_date = price_alerts.created_at.date()
                print(f"Fetched old price: {old_price}, Fetched price date: {price_date}")  # Debugging

                # If the stored price is from a previous day, update the stored price with today's new price
                if price_date != today:
                    print(f"Updating opening price for the day to: {new_price}")
                    AdminPriceAlerts.objects.create(content="Opening price for the day", price_inr=new_price)
                    old_price = new_price  # Set old_price to today's new price for further comparisons in the day
            except AdminPriceAlerts.DoesNotExist:
                # If no previous price exists, store the current price as the first price of the day
                old_price = None

            # If old_price is None, store the current price as the first price of the day and return
            if old_price is None:
                AdminPriceAlerts.objects.create(content="First price of the day", price_inr=new_price)
                return Response({
                    "message": "No previous price to compare. Stored the current price as the first price of the day.",
                    "new_price": new_price
                }, status=status.HTTP_200_OK)

            # Calculate the price change from the opening price
            price_change = calculate_change(old_price, new_price)

            # Check if price change exceeds the threshold (5% increase or decrease)
            if abs(price_change) >= 0.30:
                direction = "increased" if price_change > 0 else "decreased"
                # For each user, send a message to RabbitMQ
                for user_id in user_ids:
                    notification_data = {
                        "user_id": user_id,
                        "content": f"Ethereum price {direction} by {price_change:.2f}% (New Price: ₹{new_price})"
                    }
                    # Publish the message to RabbitMQ
                    publish_to_rabbitmq(json.dumps(notification_data))

                # Update the latest price in AdminPriceAlerts
                AdminPriceAlerts.objects.create(content=f"Price updated to ₹{new_price}", price_inr=new_price)
                return Response({
                    "message": "Price Alerts notifications queued successfully.",
                    "price_alerts_content": f"Ethereum price {direction} by {price_change:.2f}%",
                    "new_price": new_price
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "message": f"Price change of {price_change:.2f}% does not exceed the 5% threshold.",
                    "new_price": new_price
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
                print("No users with price alerts enabled.")  # Debugging
                return Response({'error': 'No users with price alerts enabled.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Exception occurred while fetching user IDs for price alerts: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
