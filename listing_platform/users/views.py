from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .models import Message
from listings.models import Listing
from .forms import MessageForm, DirectMessageForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models




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
def inbox(request):
    user = request.user
    messages_qs = Message.objects.filter(
        models.Q(sender=user) | models.Q(recipient=user)
    )

    other_users = set()
    for msg in messages_qs:
        other = msg.recipient if msg.sender == user else msg.sender
        other_users.add(other)

    return render(request, 'users/inbox.html', {
        'conversation_users': sorted(other_users, key=lambda u: u.username.lower())
    })


@login_required
def conversation_with_user(request, username):
    other_user = get_object_or_404(User, username=username)

    messages_between = Message.objects.filter(
        models.Q(sender=request.user, recipient=other_user) |
        models.Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            return redirect('users:conversation', username=username)
    else:
        form = DirectMessageForm()

    return render(request, 'users/conversation.html', {
        'form': form,
        'other_user': other_user,
        'messages_between': messages_between
    })

@login_required
def my_profile(request):
    listings = Listing.objects.filter(author=request.user).order_by('-date')

    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('users:login')
    else:
        form = SetPasswordForm(user=request.user)

    return render(request, 'users/my_profile.html', {
        'listings': listings,
        'form': form
    })