from django.shortcuts import render, get_object_or_404
from .models import Tour
# Create your views here.

def tourList(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})