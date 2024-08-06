from django.db import models

class Notification(models.Model):
    email_id = models.EmailField(unique=True)
    verification_status = models.BooleanField(default=False)
    message = models.TextField(default='OTP Message')
    type = models.CharField(max_length=50, default='OTP')
    status = models.CharField(max_length=20, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_id

class TempOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# from django.db import models

# # Create your models here.
# class Notification(models.Model):
#     email_id = models.EmailField(unique=True)
#     verification_status = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email_id

# class TempOTP(models.Model):
#     email = models.EmailField()
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.email