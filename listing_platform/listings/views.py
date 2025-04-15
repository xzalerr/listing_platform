from django.shortcuts import render
from .models import Listing

# Create your views here.
def browse_listings(request):
    listings = Listing.objects.all().order_by('-date')
    return render(request, 'listings/browse_listings.html', {'listings' : listings})

def listing_page(request, slug):
    listing = Listing.objects.get(slug=slug)
    return render(request, 'listings/listing_page.html', {'listing' : listing})