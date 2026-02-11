from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_pic/", blank=True,null=True)
    @property
    def is_agent(self):
        return self.groups.filter(name='Agent').exists()

    @property
    def is_customer(self):
        return self.groups.filter(name='Customer').exists()


class AgentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    verified = models.BooleanField(default=False)
    experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.user.username
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')

    def __str__(self):
        return self.user.username
