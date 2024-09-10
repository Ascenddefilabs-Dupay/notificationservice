from django.db import models
# Remove or comment out this line if it's not needed
# from PushNotification1.models import EmailVerificationNotification, NotificationSettings

class NotificationSettings(models.Model):
    user_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    messages = models.BooleanField(default=True)
    product_announcement = models.BooleanField(default=True)
    special_offers = models.BooleanField(default=True)
    insights_tips = models.BooleanField(default=True)
    price_alerts = models.BooleanField(default=True)
    account_activity = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification_settings'

    def __str__(self):
        return f'Notification Settings for {self.user_id}'


class AdminMessages(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_messages'

    def __str__(self):
        return f'Messages created at {self.created_at}'

class MessagesNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages_notifications'

    def __str__(self):
        return str(self.notification_id)

    def save(self, *args, **kwargs):
        # Ensure that each user has at most 5 notifications stored
        notifications_count = MessagesNotifications.objects.filter(user_id=self.user_id).count()
        if notifications_count >= 5:
            oldest_notification = MessagesNotifications.objects.filter(user_id=self.user_id).order_by('created_at').first()
            oldest_notification.delete()

        # Generate unique notification ID
        if not self.notification_id:
            last_notification = MessagesNotifications.objects.all().order_by('notification_id').last()

            if last_notification:
                last_id = last_notification.notification_id
                id_number = int(last_id.split('NOTMS')[-1]) + 1
            else:
                id_number = 1

            self.notification_id = f'NOTMS{id_number:05d}'

        super(MessagesNotifications, self).save(*args, **kwargs)
