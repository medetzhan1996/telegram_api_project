from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationAPIView

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
]