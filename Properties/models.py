from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

type = (
    ('Rent', 'Rent'),
    ('For Sale', 'For Sale'),
)


class Properties(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, blank=True, null=True)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bedrooms = models.IntegerField(null=True,blank=True)
    living_rooms = models.IntegerField(null=True,blank=True)
    Sqm = models.IntegerField(null=True,blank=True)
    bathrooms = models.IntegerField(null=True,blank=True)
    property_type = models.CharField(max_length=20, choices=type, default='rent', null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)



    def __str__(self):
        return self.title
    
