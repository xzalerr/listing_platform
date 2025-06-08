from django import forms
from .models import Listing

class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'picture']
