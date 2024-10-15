# cryptoalerts/serializers.py
from rest_framework import serializers
from .models import PriceAlertsNotifications, AdminManageCryptoCurrencies, AdminPriceAlerts

class PriceAlertsNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlertsNotifications
        fields = '__all__'

class AdminManageCryptoCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminManageCryptoCurrencies
        fields = '__all__'
        read_only_fields = ('currency_id', 'last_notified_date')  # Make currency_id and last_notified_date read-only

    def validate_symbol(self, value):
        if not value.isupper() or len(value) != 3:
            raise serializers.ValidationError("Symbol must be a unique, 3-letter uppercase code.")
        return value

    def validate_price_change_threshold(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price change threshold must be positive.")
        return value

    def validate_coin_gecko_id(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("CoinGecko ID must be a valid string.")
        return value

class AdminPriceAlertsSerializer(serializers.ModelSerializer):
    currency = AdminManageCryptoCurrenciesSerializer()

    class Meta:
        model = AdminPriceAlerts
        fields = '__all__'







# # serializers.py
# from rest_framework import serializers
# from .models import PriceAlertsNotifications, AdminManageCryptoCurrencies, AdminPriceAlerts

# class PriceAlertsNotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PriceAlertsNotifications
#         fields = '__all__'

# class AdminManageCryptoCurrenciesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdminManageCryptoCurrencies
#         fields = '__all__'
#         read_only_fields = ('currency_id',)  # Make currency_id read-only

#     def validate_symbol(self, value):
#         if not value.isupper() or len(value) != 3:
#             raise serializers.ValidationError("Symbol must be a unique, 3-letter uppercase code.")
#         return value

#     def validate_price_change_threshold(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Price change threshold must be positive.")
#         return value

#     def validate_coin_gecko_id(self, value):
#         if not value or len(value.strip()) == 0:
#             raise serializers.ValidationError("CoinGecko ID must be a valid string.")
#         return value

# class AdminPriceAlertsSerializer(serializers.ModelSerializer):
#     currency = AdminManageCryptoCurrenciesSerializer()

#     class Meta:
#         model = AdminPriceAlerts
#         fields = '__all__'
