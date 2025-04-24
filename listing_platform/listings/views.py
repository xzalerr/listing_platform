from django.shortcuts import render, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def browse_listings(request):
    listings = Listing.objects.all().order_by('-date')
    return render(request, 'listings/browse_listings.html', {'listings' : listings})

def listing_page(request, slug):
    listing = Listing.objects.get(slug=slug)
    return render(request, 'listings/listing_page.html', {'listing' : listing})

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