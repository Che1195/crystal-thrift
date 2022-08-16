from django import forms
from .models import UserProfile

# TODO
# create validators for
#   - email, building, floor 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture',
                'email', 'building', 'floor']
    
    def clean(self):
        """making sure all data being submitted is eligible"""
        pass