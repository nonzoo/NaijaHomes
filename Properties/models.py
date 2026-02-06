from django.db import models
from django.contrib.auth.models import User
from django.conf import settings




class Properties(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/')



    def __str__(self):
        return self.title
    
