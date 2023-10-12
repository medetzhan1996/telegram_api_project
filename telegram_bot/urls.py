from django.urls import path

from telegram_bot.views import GenerateTokenView, TelegramWebhook, CreateUserMessageView, UserMessageListView

urlpatterns = [
    path('generate-token/', GenerateTokenView.as_view(), name='generate_token'),
    path('send_message/', CreateUserMessageView.as_view(), name='send_message'),
    path('messages/', UserMessageListView.as_view(), name='usermessage-list'),
    path('webhook/', TelegramWebhook.as_view(), name='telegram_webhook'),
]
