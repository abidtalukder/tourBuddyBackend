from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tour, Landmark
from .serializers import TourSerializer, LandmarkSerializer

# Create your views here.
# def tourList(request):
#     tours = Tour.objects.all()
#     return render(request, 'tours/tourList.html', {'tours': tours})

# def tourDetail(request, tourID):
#     tour = get_object_or_404(Tour, pk=tourID)
#     return render(request, 'tours/tourDetail.html', {'tour': tour})

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