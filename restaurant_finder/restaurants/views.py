# restaurants/views.py

from django.shortcuts import render, get_object_or_404
import requests
from django.conf import settings
from .forms import RestaurantSearchForm
from .models import Restaurant, Review
from datetime import datetime
from geopy.distance import geodesic


def home(request):
    return render(request, 'restaurants/home.html')


def search_restaurants(request):
    form = RestaurantSearchForm(request.GET)
    restaurants = []

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        cuisine_type = form.cleaned_data.get('cuisine_type')
        min_rating = form.cleaned_data.get('min_rating')
        max_distance = form.cleaned_data.get('max_distance')

        # Get user's location from the request
        user_lat = request.GET.get('user_lat')
        user_lng = request.GET.get('user_lng')

        if user_lat and user_lng:
            user_location = (float(user_lat), float(user_lng))
        else:
            # Default location if geolocation fails
            user_location = (40.7128, -74.0060)  # New York City

        # Combine search query and cuisine type
        query = f"{search_query} {cuisine_type}".strip()
        if query:
            query += " restaurant"
        else:
            query = "restaurant"  # Default search if both fields are empty

        # Make a request to the Google Places API
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': settings.GOOGLE_MAPS_API_KEY,
            'location': f"{user_lat},{user_lng}",
            'radius': 50000  # 50km radius, adjust as needed
        }
        response = requests.get(url, params=params)
        results = response.json().get('results', [])

        for result in results:
            # Extract types from the result
            types = result.get('types', [])

            # Try to determine a more specific cuisine type
            specific_cuisine = next((t for t in types if t.endswith('_restaurant')), None)
            if specific_cuisine:
                result_cuisine = specific_cuisine.replace('_', ' ').title()
            elif cuisine_type:
                result_cuisine = cuisine_type
            else:
                result_cuisine = 'Restaurant'

            restaurant, created = Restaurant.objects.update_or_create(
                place_id=result['place_id'],
                defaults={
                    'name': result['name'],
                    'address': result['formatted_address'],
                    'latitude': result['geometry']['location']['lat'],
                    'longitude': result['geometry']['location']['lng'],
                    'rating': result.get('rating', 0.0),
                    'cuisine_type': result_cuisine,
                }
            )

            # Calculate distance
            restaurant_location = (restaurant.latitude, restaurant.longitude)
            distance = geodesic(user_location, restaurant_location).km

            # Apply filters
            if min_rating and restaurant.rating < min_rating:
                continue
            if max_distance and distance > max_distance:
                continue

            restaurant.distance = distance  # Add distance to the restaurant object
            restaurants.append(restaurant)

        # Sort restaurants by distance
        restaurants.sort(key=lambda x: x.distance)

    context = {
        'form': form,
        'restaurants': restaurants,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'user_lat': user_lat,
        'user_lng': user_lng
    }
    return render(request, 'restaurants/search_results.html', context)


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Fetch detailed information from Google Places API
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': restaurant.place_id,
        'fields': 'name,formatted_address,formatted_phone_number,website,rating,price_level,review',
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    place_details = response.json().get('result', {})

    # Update restaurant details
    restaurant.phone_number = place_details.get('formatted_phone_number', '')
    restaurant.website = place_details.get('website', '')
    restaurant.google_rating = place_details.get('rating')
    restaurant.price_level = place_details.get('price_level')
    restaurant.save()

    # Fetch and save reviews
    reviews = place_details.get('reviews', [])
    for review_data in reviews:
        Review.objects.update_or_create(
            restaurant=restaurant,
            author_name=review_data['author_name'],
            defaults={
                'rating': review_data['rating'],
                'text': review_data['text'],
                'time': datetime.fromtimestamp(review_data['time'])
            }
        )

    context = {
        'restaurant': restaurant,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'reviews': restaurant.reviews.all().order_by('-time')[:5]  # Get the 5 most recent reviews
    }
    return render(request, 'restaurants/restaurant_detail.html', context)