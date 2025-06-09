from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:username>/', views.conversation_with_user, name='conversation'),
    path('my-profile/', views.my_profile, name='my-profile')
]

