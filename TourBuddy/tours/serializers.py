from rest_framework import serializers
from .models import Tour, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'description']

class TourSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)  # Include related locations in each tour
    class Meta:
        model = Tour
        fields = ['title', 'landmarks']
