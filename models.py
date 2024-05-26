from django.db import models
from django.core.validators import URLValidator
import secrets

class Account(models.Model):
    email = models.EmailField(unique=True)  
    account_id = models.CharField(max_length=255, unique=True)  
    account_name = models.CharField(max_length=255)  
    app_secret_token = models.CharField(max_length=255, default="generate_unique_token")  
    website = models.URLField(blank=True)  

    def __str__(self):
        return self.account_name

    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = generate_unique_token()
        super().save(*args, **kwargs)

def generate_unique_token():
    return secrets.token_urlsafe(64)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Link to the associated account
    platform_name = models.CharField(max_length=255)
    webhook_url = models.CharField(max_length=1024, validators=[URLValidator()])  # Validated URL
    credentials = models.TextField(blank=True)  # Optional credentials (securely stored)

    def __str__(self):
        return f"{self.platform_name} ({self.account.account_name})"
