from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    referral_code = models.CharField(max_length=10, blank=True, null=True)

class Referral(models.Model):
    referring_user = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
