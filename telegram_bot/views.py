import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import TelegramProfile, UserMessage
from .serializers import TelegramProfileSerializer, UserMessageSerializer
from .services import TelegramService, TelegramProfileService


class GenerateTokenView(generics.CreateAPIView):
    queryset = TelegramProfile.objects.all()
    serializer_class = TelegramProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        profile, created = TelegramProfile.objects.get_or_create(user=request.user)
        profile.generate_token()
        return Response({"token": profile.token})


class UserMessageListView(generics.ListAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateUserMessageView(generics.CreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Сохраняет сообщение и отправляет его в Telegram."""
        serializer.save(user=self.request.user)
        self.status_message = TelegramService.send_message(
            self.request.user, serializer.validated_data['message_body'])

    def create(self, request, *args, **kwargs):
        """Создает новое сообщение и возвращает ответ с дополнительным статусом."""
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.data['status_message'] = self.status_message
        return response


class TelegramWebhook(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = json.loads(json_str)
        TelegramProfileService.handle_webhook(update)
        return JsonResponse({"status": "ok"})
