from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='media/database_error.jpg', upload_to='main_images/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    PRICE_CHOICES = [
        ('exchange', 'Exchange'),
    ]

    price_value = models.FloatField(null=True, blank=True)
    price_option = models.CharField(max_length=10, choices=PRICE_CHOICES, null=True, blank=True)

    def display_price(self):
        if self.price_option == 'exchange':
            return "Exchange"
        elif self.price_value is not None:
            return f"{self.price_value:.2f} zł"
        return "No price"

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return f"{self.listing.title} – image {self.pk}"