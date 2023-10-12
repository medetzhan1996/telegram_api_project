from rest_framework import serializers
from telegram_bot.models import TelegramProfile, UserMessage


class TelegramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramProfile
        fields = ['user', 'telegram_id', 'token']


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['date', 'message_body']
