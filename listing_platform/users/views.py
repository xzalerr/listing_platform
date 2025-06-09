from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages



# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('listings:list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { "registration": form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('listings:list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "login": form })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('listings:list')
    
@login_required
@login_required
def send_message(request):
    error = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['recipient_username']
            body = form.cleaned_data['body']
            try:
                recipient = User.objects.get(username=username)
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    body=body
                )
                messages.success(request, f"Message sent to {username}")
                return redirect('users:inbox')
            except User.DoesNotExist:
                error = f"No such user: {username}"
    else:
        form = MessageForm()

    return render(request, 'users/send_message.html', {'form': form, 'error': error})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'users/inbox.html', {'messages': messages})