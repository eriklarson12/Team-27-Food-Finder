# restaurants/forms.py

from django import forms

class RestaurantSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)
    cuisine_type = forms.CharField(label='Cuisine Type', max_length=100, required=False)
    min_rating = forms.FloatField(label='Minimum Rating', min_value=0, max_value=5, required=False)
    max_distance = forms.FloatField(label='Maximum Distance (km)', min_value=0, required=False)