from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.browse_listings, name='list'),
    path('listing-new/', views.listing_new, name='listing-new'),
    path('<slug:slug>', views.listing_page, name='page'),
    path('listing-edit/<slug:slug>/', views.listing_edit, name='listing-edit'),
    path('listing-delete/<slug:slug>/', views.listing_delete, name='listing-delete'),
    path('image/<int:pk>/delete/', views.delete_listing_image, name='listing-image-delete')
]
