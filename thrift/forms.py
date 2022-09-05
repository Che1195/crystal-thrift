from django import forms
from .models import UserProfile, Item
from datetime import datetime



# TODO
# create validators for
#   - email, building, floor 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ['user', 'slug', 'modified']
    
    def clean(self):
        """making sure all data being submitted is eligible"""
        pass

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['user', 'slug', 'modified', 'sale_status']
    
    def clean(self):
        """making sure all data being submitted is eligible"""
        pass

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['user', 'slug', 'modified']
