# restaurants/urls.py

from django.urls import path
from . import views

app_name = 'restaurants'  # This sets the namespace for your app's URLs

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_restaurants, name='search'),  # Changed to 'search/'
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail')
]