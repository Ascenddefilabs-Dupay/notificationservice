
from django.db import models

class EmailVerificationNotification(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    email_id = models.EmailField()
    message = models.TextField()
    type = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification'

    def __str__(self):
        return str(self.notification_id)

    def save(self, *args, **kwargs):
        if not self.notification_id:
            last_notification = EmailVerificationNotification.objects.all().order_by('notification_id').last()
            
            if last_notification:
                last_id = last_notification.notification_id
                id_number = int(last_id.split('NOT')[-1]) + 1
            else:
                id_number = 1

            self.notification_id = f'NOT{id_number:04d}'
        
        super(EmailVerificationNotification, self).save(*args, **kwargs)

class NotificationSettings(models.Model):
    user_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    messages = models.BooleanField(default=True)
    product_announcement = models.BooleanField(default=True)
    special_offers = models.BooleanField(default=True)
    insights_tips = models.BooleanField(default=True) 

    class Meta:
        db_table = 'notification_settings'

    def __str__(self):
        return f'Notification Settings for {self.user_id}'
