from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Add extra fields or methods as needed in future.
    """
    pass