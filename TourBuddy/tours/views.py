from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tour, Landmark
from .serializers import TourSerializer, LandmarkSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import generateLandmarks

class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class LandmarkListCreateView(generics.ListCreateAPIView):
    queryset = Landmark.objects.all()
    serializer_class = LandmarkSerializer

class LandmarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Landmark.objects.all()
    serializer_class = LandmarkSerializer

def home(request):
    return HttpResponse("Welcome to TourBuddy API!")

def getRoute(request):
    startingLocation = "lat: 42.72961654355887 lng: -73.68126988771975"
    return JsonResponse(generateLandmarks.generateLandmarks(startingLocation))