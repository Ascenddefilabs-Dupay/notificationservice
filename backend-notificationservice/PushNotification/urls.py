# PushNotification/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SaveTokenView, SendNotificationView
from .views import save_token

urlpatterns = [
    path('save-token/', save_token, name='save_token'),
    path('send-notification/', SendNotificationView.as_view(), name='send_notification'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # notifications/urls.py
# from django.urls import path
# from .views import SaveTokenView, SendNotificationView

# urlpatterns = [
#     path('save-token/', SaveTokenView.as_view(), name='save-token'),
#     path('send-notification/', SendNotificationView.as_view(), name='send-notification'),
# ]
