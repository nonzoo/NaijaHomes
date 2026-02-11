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
    is_featured = models.BooleanField(default=False, blank=True)
    
    
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def __str__(self):
        return self.title
    



class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey("Properties", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "property")

    def __str__(self):
        return f"{self.user} saved {self.property}"

