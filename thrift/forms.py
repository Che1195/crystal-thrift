from django import forms
from .models import UserProfile, Item, ItemImage
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

class ItemImageForm(forms.ModelForm):
    image = forms.ImageField(
        label = "Image",
        widget = forms.ClearableFileInput(attrs={"multiple": True}), # "multiple" allows us to use have multiple files get uploaded in the input field
    )

    class Meta:
        model = ItemImage
        fields = ["image"]
