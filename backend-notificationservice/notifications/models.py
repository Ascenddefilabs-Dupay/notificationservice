from django.db import models

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)  # Explicitly declare the primary key
    wallet_id = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    transaction_currency = models.CharField(max_length=50)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_timestamp = models.DateTimeField()
    transaction_status = models.CharField(max_length=50)
    user_phone_number = models.CharField(max_length=20)
    sender_mobile_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'transaction_table'
        managed = False


class PriceAlertsNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_alerts_notifications'
        managed = False


class MessagesNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages_notifications'
        managed = False
    
class SpecialOffersNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'special_offers_notifications'
        managed = False


class ProductAnnouncementNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_announcement_notifications'
        managed = False

class InsightsTipsNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'insights_tips_notifications'
        managed = False


class AccountActivityNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'account_activity_notifications'
        managed = False