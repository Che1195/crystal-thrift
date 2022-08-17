from django.conf import settings
from django.db import models
from .utils import CHOICES

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/") 
    email = models.EmailField(max_length=128)
    building = models.CharField(blank=True, null=True, choices=CHOICES['building'], max_length=1)
    floor = models.CharField(blank=True, null=True, choices=CHOICES['floor'], max_length=2)

    def get_absolute_url(self):
        """takes you to the user's profile page"""
        pass

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=128)
    description = models.TextField(null=True, max_length=512)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")
    condition = models.CharField(null=True, max_length=20, choices=CHOICES['condition'])
    item_type = models.CharField(null=True, max_length=20, choices=CHOICES['item-type'])
    price = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    