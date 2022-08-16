from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name']
    raw_id_fields = ['user']

admin.site.register(UserProfile, UserProfileAdmin)  