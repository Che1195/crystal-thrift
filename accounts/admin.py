from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import UserProfile


    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=128)
    # last_name = models.CharField(max_length=128)
    # profile_picture = models.ImageField(null=True, blank=True) 
    # email = models.EmailField(max_length=128)
    # building = models.IntegerField(blank=True, null=True)
    # floor = models.IntegerField(blank=True, null=True)
    # slug = models.SlugField(blank=True, null=True, unique=True)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name']
    raw_id_fields = ['user']

admin.site.register(UserProfile, UserProfileAdmin)  