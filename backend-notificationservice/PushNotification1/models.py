from django.db import models
import uuid

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


# from django.db import models
# import uuid

# class EmailVerificationNotification(models.Model):
#     notification_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     user_id = models.CharField(max_length=255, null=True, blank=True)  # Allow null and blank
#     email_id = models.EmailField()
#     message = models.TextField()
#     type = models.CharField(max_length=255)  # Add the type field
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)  # Add updated_at field

#     class Meta:
#         db_table = 'notification'

#     def __str__(self):
#         return str(self.notification_id)


# from django.db import models

# class EmailVerificationNotification(models.Model):
#     notification_id = models.CharField(max_length=10, unique=True, editable=False)
#     email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     email = models.EmailField()
#     message = models.TextField()
#     notification_id = models.CharField(max_length=10, unique=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.notification_id:
#             last_notification = EmailVerificationNotification.objects.all().order_by('id').last()
#             if last_notification:
#                 last_id = last_notification.notification_id
#                 notification_number = int(last_id.replace('NOT', '')) + 1
#                 self.notification_id = 'NOT{:04d}'.format(notification_number)
#             else:
#                 self.notification_id = 'NOT0001'
#         super(EmailVerificationNotification, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.notification_id
