from rest_framework import serializers
from .models import Tour, Landmark

class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = ['name', 'description', "latitude", "longitude"]

class TourSerializer(serializers.ModelSerializer):
    landmarks = LandmarkSerializer(many=True)  # Include related locations in each tour
    class Meta:
        model = Tour
        fields = ['title', 'landmarks']
