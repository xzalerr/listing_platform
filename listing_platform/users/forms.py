from django import forms
from .models import Message

class MessageForm(forms.Form):
    recipient_username = forms.CharField(label="Recipient Username", max_length=150)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Message")
