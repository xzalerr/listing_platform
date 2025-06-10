from django import forms
from .models import Listing

class CreateListing(forms.ModelForm):
    price_value = forms.FloatField(required=False, label='Price (PLN)')
    price_option = forms.ChoiceField(
        choices=[('', '---'), ('exchange', 'Exchange')],
        required=False,
        label='Price Option'
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'picture', 'price_value', 'price_option']
