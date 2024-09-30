# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Favorite
from restaurants.models import Restaurant
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'favorites': favorites,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def toggle_favorite(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    if not created:
        favorite.delete()

    return redirect(reverse('restaurants:restaurant_detail', kwargs={'restaurant_id': restaurant_id}))


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'favorites_list.html', {'favorites': favorites})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('restaurants:home')
    else:
        return redirect('restaurants:home')