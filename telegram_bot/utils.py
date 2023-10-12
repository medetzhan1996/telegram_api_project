import telebot
from decouple import config
from .models import TelegramProfile


def send_telegram_message(user, message_body):
    """Отправляет сообщение пользователю в Telegram."""
    try:
        telegram_profile = TelegramProfile.objects.get(user=user)
        telegram_id = telegram_profile.telegram_id
    except TelegramProfile.DoesNotExist:
        print(f"No Telegram profile found for user: {user}")
        return

    # Форматируем сообщение
    message = f"{user.first_name}, я получил от тебя сообщение:\n{message_body}"

    bot_token = config('TELEGRAM_BOT_TOKEN')
    bot = telebot.TeleBot(bot_token)

    bot.send_message(chat_id=telegram_id, text=message)
