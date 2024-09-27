# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='restaurants:home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorite/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorite/toggle/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite')
]