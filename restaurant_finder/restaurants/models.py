# restaurants/models.py

from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    cuisine_type = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(default=0.0)
    place_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    google_rating = models.FloatField(null=True, blank=True)
    price_level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.author_name}'s review for {self.restaurant.name}"