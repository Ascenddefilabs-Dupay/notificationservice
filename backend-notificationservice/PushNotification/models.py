# notifications/models.py
from django.db import models
# from django.utils import timezone

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_token = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class FCMToken(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token