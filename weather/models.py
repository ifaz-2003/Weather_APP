from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    REQUIRED_FIELDS = ['email']  # Makes email required

class SavedCity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    temp = models.FloatField(default=0.0)  # Set a default value
    description = models.CharField(max_length=255, null=True, blank=True)
    icon = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.city_name}"