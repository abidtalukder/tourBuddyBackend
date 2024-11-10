from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from .models import Tour, Location
from .serializers import TourSerializer, LocationSerializer

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

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
