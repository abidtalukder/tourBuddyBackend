from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *

from django.shortcuts import render
from django.http import JsonResponse
import json
import random 

# Create your views here.
def tourList(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})

def tourDetail(request, tourID):
    tour = get_object_or_404(Tour, pk=tourID)
    return render(request, 'tours/tour_detail.html', {'tour': tour})
def signUp():
    pass
def logIn():
    pass

@csrf_exempt
def submitRatings(request):
    
    newReview = json.loads(request.body)
   # newReview = {"user":"munzir", "rating":100, "city":"Troy", "journal":"it was fun"}
    try:
        city = Location.objects.get(city=newReview["city"])
        city.total += 1
        city.rating = (city.rating * (city.total - 1) + newReview["rating"])/city.total
        print((city.rating * (city.total - 1) + newReview["rating"])/city.total)
        if not newReview["user"] in json.loads(city.users)["users"]:
            temp = json.loads(city.users)
            temp["users"].append(newReview["user"])
            city.users = json.dumps(temp)
        if newReview["journal"] != "":
            temp = json.loads(city.journal)
            temp["entries"].append(newReview["journal"])
            city.journal = json.dumps(temp)
    except:
        city =  Location(city=newReview["city"],rating=newReview["rating"],total=1,users=json.dumps({"users":[newReview["user"]]}),
                       journal=json.dumps({"entries":[newReview["journal"]]}))
    city.save()
    return JsonResponse({'resp': "hi"})
    