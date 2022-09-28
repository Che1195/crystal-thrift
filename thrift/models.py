from django.conf import settings
from django.db import models
from django.utils import timezone

import uuid

from .utils import CHOICES

User = settings.AUTH_USER_MODEL
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(default=uuid.uuid4, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/") 
    email = models.EmailField(max_length=128)
    building = models.CharField(blank=True, null=True, choices=CHOICES['building'], max_length=1)
    floor = models.CharField(blank=True, null=True, choices=CHOICES['floor'], max_length=2)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """takes you to the user's profile page"""
        return f"/thrift/profile-detail/{self.slug}"

class Item(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, default=uuid.uuid4)    
    title = models.CharField(null=True, max_length=128)
    description = models.TextField(null=True, max_length=512)
    condition = models.CharField(null=True, max_length=20, choices=CHOICES['condition'])
    item_type = models.CharField(null=True, max_length=20, choices=CHOICES['item-type'])
    price = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    sale_status = models.CharField(null=True, max_length=20, choices=CHOICES['sale-status'], default="available")
    created = models.DateTimeField(null=True, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=True, auto_now=True)
    date_sold = models.DateTimeField(null=True, blank=True, editable=False) # a date is given when the sold switch is flicked

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        """takes you to the user's profile page"""
        return f"/thrift/item-detail/{self.slug}"

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # updating the created and modified timestamp fields
        if not self.id: 
            # if the item does not have an id field 
            # give the created field the current time
            self.created = timezone.now()
        self.modified = timezone.now()
        # changing the date_sold field based on changes to the sale_status
        if self.sale_status == "sold":
            self.date_sold = timezone.now()
        else:
            self.date_sold = None 
        return super().save(*args, **kwargs)

class ItemImage(models.Model):
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE, related_name="item_images")
        # added related related_name="item_images" for referencing the child from the parent in templates
    image = models.ImageField(null=True, blank=True, upload_to="images/")

        

    