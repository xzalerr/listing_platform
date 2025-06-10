from django import forms
from .models import Message, UserRating

class MessageForm(forms.Form):
    recipient_username = forms.CharField(label="Recipient Username", max_length=150)
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Message")


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your message...'})
        }

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, str(i)) for i in range(1, 6)])
        }
        labels = {
            'score': 'Rate this user (1–5)'
        }
