from django.core.management.base import BaseCommand
import telebot
from decouple import config


class Command(BaseCommand):
    help = 'Set the Telegram bot webhook'

    def add_arguments(self, parser):
        parser.add_argument('webhook_url', type=str, help='URL for the Telegram bot webhook')

    def set_webhook(self, webhook_url):
        bot_token = config('TELEGRAM_BOT_TOKEN')
        bot = telebot.TeleBot(bot_token)
        bot.set_webhook(url=webhook_url)

    def handle(self, *args, **kwargs):
        webhook_url = kwargs['webhook_url']
        self.set_webhook(webhook_url)
        self.stdout.write(self.style.SUCCESS(f'Webhook set to {webhook_url} successfully!'))