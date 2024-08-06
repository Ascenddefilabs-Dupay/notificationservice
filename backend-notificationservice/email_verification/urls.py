from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VerifyEmailView

router = DefaultRouter()

urlpatterns = [
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    # path('api/verify-email/', verify_email, name='verify-email'),
]

urlpatterns += router.urls
