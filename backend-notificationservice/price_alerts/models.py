from django.db import models
from PushNotification1.models import NotificationSettings

class AdminManageCryptoCurrencies(models.Model):
    currency_id = models.CharField(max_length=6, unique=True, primary_key=True)
    symbol = models.CharField(max_length=10, unique=True)  # e.g., BTC, ETH
    coin_gecko_id = models.CharField(max_length=50, unique=True)  # e.g., bitcoin, ethereum
    price_change_threshold = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_manage_crypto_currencies'

    def __str__(self):
        return self.symbol

    def save(self, *args, **kwargs):
        if not self.currency_id:
            last_currency = AdminManageCryptoCurrencies.objects.all().order_by('currency_id').last()
            if last_currency:
                last_id = last_currency.currency_id
                id_number = int(last_id.replace('CUR', '')) + 1
            else:
                id_number = 1
            self.currency_id = f'CUR{id_number:03d}'
        self.symbol = self.symbol.upper()
        super(AdminManageCryptoCurrencies, self).save(*args, **kwargs)

class AdminPriceAlerts(models.Model):
    content = models.TextField()
    currency = models.ForeignKey(AdminManageCryptoCurrencies, on_delete=models.CASCADE)
    price_inr = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_price_alerts'

    def __str__(self):
        return f'Price Alert for {self.currency.symbol} at {self.created_at}'

class PriceAlertsNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_alerts_notifications'

    def __str__(self):
        return str(self.notification_id)

    def save(self, *args, **kwargs):
        # Ensure that each user has at most 5 notifications stored
        notifications_count = PriceAlertsNotifications.objects.filter(user_id=self.user_id).count()
        if notifications_count >= 5:
            oldest_notification = PriceAlertsNotifications.objects.filter(user_id=self.user_id).order_by('created_at').first()
            oldest_notification.delete()

        # Generate unique notification ID
        if not self.notification_id:
            last_notification = PriceAlertsNotifications.objects.all().order_by('notification_id').last()
            if last_notification:
                last_id = last_notification.notification_id
                id_number = int(last_id.split('NOTPA')[-1]) + 1
            else:
                id_number = 1
            self.notification_id = f'NOTPA{id_number:05d}'

        super(PriceAlertsNotifications, self).save(*args, **kwargs)
