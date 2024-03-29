from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

# for image deletion functionality
from django.db.models.signals import post_delete
from django.dispatch import receiver

import uuid
import pathlib

from .utils import CHOICES

User = settings.AUTH_USER_MODEL

# Query Managers
class ItemQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) 
            # add more lookup parameters
        )
        return self.filter(lookups)

class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self.db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(default=uuid.uuid4, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/")
    contact_method = models.TextField(default="contact me at...", max_length=256)
    email = models.EmailField(max_length=128)
    # building = models.CharField(blank=True, null=True, choices=CHOICES['building'], max_length=1)
    # floor = models.CharField(blank=True, null=True, choices=CHOICES['floor'], max_length=2)
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
    title = models.CharField(null=True, max_length=64)
    description = models.TextField(null=True, max_length=512)
    condition = models.CharField(null=True, max_length=20, choices=CHOICES['condition'])
    item_type = models.CharField(null=True, max_length=20, choices=CHOICES['item-type'])
    price = models.DecimalField(null=True, max_digits=9, decimal_places=2)
    sale_status = models.CharField(null=True, max_length=20, choices=CHOICES['sale-status'], default="available")
    image1 = models.ImageField(null=True, blank=False, upload_to="images/") 
    image2 = models.ImageField(null=True, blank=True, upload_to="images/") 
    image3 = models.ImageField(null=True, blank=True, upload_to="images/") 
    image4 = models.ImageField(null=True, blank=True, upload_to="images/") 
    image5 = models.ImageField(null=True, blank=True, upload_to="images/") 
    created = models.DateTimeField(null=True, editable=False, auto_now_add=True)
    modified = models.DateTimeField(null=True, auto_now=True)
    date_sold = models.DateTimeField(null=True, blank=True, editable=False) # a date is given when the sold switch is flicked

    objects = ItemManager()
    
    def __str__(self):
        return f"{self.title}"

    @property
    def name(self):
        return self.title
    
    def get_absolute_url(self):
        """takes you to the user's profile page"""
        return f"/thrift/item-detail/{self.slug}"

    def get_absolute_user_profile_url(self):
        """takes you to the user's profile page"""
        user_profile = UserProfile.objects.get(user=self.user)
        return f"/thrift/profile-detail/{user_profile.slug}"

    def get_absolute_user_profile(self):
        return UserProfile.objects.get(user=self.user)

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

def item_image_upload_handler(instance, filename):
    file_prefix = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"images/{file_prefix}-{filename}" # creates a new file path for the upload upload adding the uuid to its original name

# class ItemImage(models.Model):
#     item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE, related_name="item_images")
#         # added related related_name="item_images" for referencing the child from the parent in templates
#     image = models.ImageField(null=True, blank=True, upload_to=item_image_upload_handler)
#         # this class has built in file type validation


####### Un-used Image Delete Automation ########################################

# src -> https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/

""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)
            
""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            #its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

""" Only delete the file if no other instances of that model are using it"""    
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)





        

    