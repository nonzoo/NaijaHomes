from django.db import models
from django.conf import settings

class AgentProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    experience = models.IntegerField(max_length=2, default=0)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    

class CustomerProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
