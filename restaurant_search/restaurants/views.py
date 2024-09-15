from django.shortcuts import render
from .models import Restaurant

def search_restaurants(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    if query:
        restaurants = Restaurant.objects.filter(
            name__icontains=query) | Restaurant.objects.filter(
            location__icontains=query) | Restaurant.objects.filter(
            cuisine__icontains=query)
    else:
        restaurants = Restaurant.objects.all()
    
    return render(request, 'restaurants/search_results.html', {'restaurants': restaurants, 'query': query})
