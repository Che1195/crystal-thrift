from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from .models import UserProfile, Item

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'user', 'first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name']
    raw_id_fields = ['user']

admin.site.register(UserProfile, UserProfileAdmin)  

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'condition', 'price']
    readonly_fields = ['created', 'modified', 'date_sold', 'slug']

admin.site.register(Item, ItemAdmin)  