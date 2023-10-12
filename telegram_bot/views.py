import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import TelegramProfile, UserMessage
from .serializers import TelegramProfileSerializer, UserMessageSerializer
from .utils import send_telegram_message


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
        serializer.save(user=self.request.user)
        send_telegram_message(self.request.user, serializer.validated_data['message_body'])


class TelegramWebhook(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = json.loads(json_str)

        if 'message' in update:
            user_data = update['message']['from']
            telegram_id = user_data['id']
            token = update['message']['text']

            try:
                profile = TelegramProfile.objects.get(token=token)
                profile.telegram_id = telegram_id
                profile.save()
            except TelegramProfile.DoesNotExist:
                pass
        return JsonResponse({"status": "ok"})
