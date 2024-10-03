# models.py
from django.db import models
from PushNotification1.models import NotificationSettings
from django.utils import timezone

class AdminSpecialOffers(models.Model):
    content_id = models.CharField(max_length=6, primary_key=True, unique=True, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=timezone.localtime)
    
    class Meta:
        db_table = 'admin_special_offers'
        managed = True
    
    def __str__(self):
        return f'Special Offers {self.content_id} created at {self.created_at}'
    
    def save(self, *args, **kwargs):
        if not self.content_id:
            last_content = AdminSpecialOffers.objects.all().order_by('content_id').last()
            if last_content:
                last_id_num = int(last_content.content_id.replace('CON', ''))
                new_id_num = last_id_num + 1
            else:
                new_id_num = 1
            self.content_id = f'CON{new_id_num:03d}'
        super(AdminSpecialOffers, self).save(*args, **kwargs)

class SpecialOffersNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'special_offers_notifications'
    
    def __str__(self):
        return str(self.notification_id)
    
    def save(self, *args, **kwargs):
        # Ensure that each user has at most 5 notifications stored
        notifications_count = SpecialOffersNotifications.objects.filter(user_id=self.user_id).count()
        if notifications_count >= 5:
            oldest_notification = SpecialOffersNotifications.objects.filter(user_id=self.user_id).order_by('created_at').first()
            oldest_notification.delete()
    
        # Generate unique notification ID
        if not self.notification_id:
            last_notification = SpecialOffersNotifications.objects.all().order_by('notification_id').last()
            if last_notification:
                last_id_num = int(last_notification.notification_id.replace('NOTSO', ''))
                id_number = last_id_num + 1
            else:
                id_number = 1
            self.notification_id = f'NOTSO{id_number:05d}'
    
        super(SpecialOffersNotifications, self).save(*args, **kwargs)
