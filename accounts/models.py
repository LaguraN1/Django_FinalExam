from django.contrib.auth.models import AbstractUser
from django.db import models
from urllib.parse import quote


class User(AbstractUser):
    bio = models.TextField(
        blank=True
    )

    avatar_url = models.URLField(
        blank=True
    )

    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url

        username = quote(self.username)

        return f"https://api.dicebear.com/9.x/identicon/svg?seed={username}"