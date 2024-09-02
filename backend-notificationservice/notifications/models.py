from django.db import models
from PushNotification1.models import EmailVerificationNotification, NotificationSettings

# If you have any other models specific to the notifications app, define them here.

class OtherNotification(models.Model):
    # Define fields specific to this app if needed
    pass

# If you only need to work with the imported models, you don't need to redefine them.
# You can simply import and use them wherever necessary.
