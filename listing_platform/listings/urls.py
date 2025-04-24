from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.browse_listings, name='list'),
    path('listing-new/', views.listing_new, name='listing-new'),
    path('<slug:slug>', views.listing_page, name='page')
]
