"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('emailverificationapi/',include('email_verification.urls')),
    # path('api1/',include('PushNotification.urls')),
    path('messagenotificationapi/',include('PushNotification1.urls')),
    path('productannouncementapi/',include('product_announcement.urls')),
    path('specialoffersapi/',include('special_offers.urls')),
    path('insightstipsapi/',include('insights_tips.urls')),
    path('pricealertsapi/',include('price_alerts.urls')),
    path('accountactivityapi/',include('account_activity.urls')),
    path('notificationsapi/',include('notifications.urls')),
]
