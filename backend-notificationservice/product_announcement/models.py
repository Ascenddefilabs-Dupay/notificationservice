from django.db import models
from PushNotification1.models import NotificationSettings

class AdminProductAnnouncement(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_product_announcement'
        

    def __str__(self):
        return f'Product Announcement created at {self.created_at}'

class ProductAnnouncementNotifications(models.Model):
    notification_id = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(fields=['user_id'], name='unique_user_notifications', deferrable=models.Deferrable.DEFERRED)
        # ]
        db_table = 'product_announcement_notifications'
        # managed = False

    def __str__(self):
        return str(self.notification_id)

    def save(self, *args, **kwargs):
        # Ensure that each user has at most 5 notifications stored
        notifications_count = ProductAnnouncementNotifications.objects.filter(user_id=self.user_id).count()
        if notifications_count >= 5:
            oldest_notification = ProductAnnouncementNotifications.objects.filter(user_id=self.user_id).order_by('created_at').first()
            oldest_notification.delete()

        # Generate unique notification ID
        if not self.notification_id:
            last_notification = ProductAnnouncementNotifications.objects.all().order_by('notification_id').last()

            if last_notification:
                last_id = last_notification.notification_id
                id_number = int(last_id.split('NOTPA')[-1]) + 1
            else:
                id_number = 1

            self.notification_id = f'NOTPA{id_number:05d}'

        super(ProductAnnouncementNotifications, self).save(*args, **kwargs)
