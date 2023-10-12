from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.PositiveIntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def generate_token(self):
        self.token = get_random_string(50)
        self.save()


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()
