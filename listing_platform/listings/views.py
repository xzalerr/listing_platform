from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing, ListingImage
from .forms import CreateListing
from django.http import HttpResponseForbidden

# Create your views here.
def browse_listings(request):
    listings = Listing.objects.all().order_by('-date')
    return render(request, 'listings/browse_listings.html', {'listings' : listings})

def listing_page(request, slug):
    listing = Listing.objects.get(slug=slug)
    is_author = request.user.is_authenticated and listing.author == request.user
    return render(request, 'listings/listing_page.html', {'listing' : listing, 'is_author': is_author})

@login_required
def listing_new(request):
    if request.method == 'POST':
        form = CreateListing(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            for file in request.FILES.getlist('images'):
                ListingImage.objects.create(listing=listing, image=file)
            return redirect('listings:list')
    else:
        form = CreateListing()
    return render(request, 'listings/listing_new.html', {'form': form})

@login_required
def listing_edit(request, slug):
    listing = get_object_or_404(Listing, slug=slug, author=request.user)

    if request.method == 'POST':
        form = CreateListing(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()

            # Delete selected images
            delete_ids = request.POST.get('delete_images', '')
            if delete_ids:
                ids_to_delete = [int(pk) for pk in delete_ids.split(',') if pk.isdigit()]
                ListingImage.objects.filter(id__in=ids_to_delete, listing=listing).delete()

            # Add new images
            for f in request.FILES.getlist('images'):
                ListingImage.objects.create(listing=listing, image=f)

            return redirect('listings:page', slug=listing.slug)
    else:
        form = CreateListing(instance=listing)

    return render(request, 'listings/listing_edit.html', {
        'form': form,
        'listing': listing,
    })



@login_required(login_url='/users/login/')
def listing_delete(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if listing.author != request.user:
        return redirect('listings:list')  # Redirect if the user is not the author

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:list')
    return render(request, 'listings/listing_delete.html', {'listing': listing})

@login_required
def delete_listing_image(request, pk):
    img = get_object_or_404(ListingImage, pk=pk, listing__user=request.user)
    slug = img.listing.slug
    if request.method == 'POST':
        img.delete()
    return redirect('listings:listing-edit', slug=slug)