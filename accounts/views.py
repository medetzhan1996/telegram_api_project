from rest_framework import generics, status

from .models import CustomUser
from .serializers import RegistrationSerializer


class RegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {
                'response': 'successfully registered a new user.',
                'username': response.data['username'],
                'first_name': response.data['first_name']
            }
        return response
