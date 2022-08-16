from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_picture = models.ImageField(null=True, blank=True) 
    email = models.EmailField(max_length=128)
    building = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def get_absolute_url(self):
        """takes you to the user's profile page"""
        pass