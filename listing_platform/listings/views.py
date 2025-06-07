from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def browse_listings(request):
    listings = Listing.objects.all().order_by('-date')
    return render(request, 'listings/browse_listings.html', {'listings' : listings})

def listing_page(request, slug):
    listing = Listing.objects.get(slug=slug)
    is_author = request.user.is_authenticated and listing.author == request.user
    return render(request, 'listings/listing_page.html', {'listing' : listing, 'is_author': is_author})

@login_required(login_url='/users/login/')
def listing_new(request):
    if request.method == 'POST':
        form = forms.CreateListing(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('listings:list')
    else:
        form = forms.CreateListing()
    return render(request, 'listings/listing_new.html', { 'form': form})

@login_required(login_url='/users/login/')
def listing_edit(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if listing.author != request.user:
        return redirect('listings:list')  # Redirect if the user is not the author

    if request.method == 'POST':
        form = forms.CreateListing(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:list')
    else:
        form = forms.CreateListing(instance=listing)
    return render(request, 'listings/listing_edit.html', {'form': form, 'listing': listing})

@login_required(login_url='/users/login/')
def listing_delete(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if listing.author != request.user:
        return redirect('listings:list')  # Redirect if the user is not the author

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:list')
    return render(request, 'listings/listing_delete.html', {'listing': listing})