from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tour, Landmark
from .serializers import TourSerializer, LandmarkSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import generateLandmarks
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import authenticate
import dotenv
from django.shortcuts import render
from django.http import JsonResponse
import json
import random 
import os
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
def tourDetail(request, tourID):
    tour = get_object_or_404(Tour, pk=tourID)
    return render(request, 'tours/tour_detail.html', {'tour': tour})
def signUp(request):
    userInfo = json.loads(request.body)
    try:
        newUser = User.objects.create_user(username=userInfo["username"],password=userInfo["password"])
        return JsonResponse({"next":"continue"})
    except:
        return JsonResponse({"message":"username already exists"})
    pass
def logIn(request):
    userInfo = json.loads(request.body)
    
    
    userAuth = authenticate(username=userInfo["username"],password=userInfo["password"])
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~{userAuth}~~~~~~~~~~~~~~~~~~~~")
    
    if not userAuth is  None:
        return JsonResponse({"next":"continue"})
    return JsonResponse({"next":"could not authenticate"})
        
    

@csrf_exempt
def submitRatings(request):
    
    newReview = json.loads(request.body)
    # routeid - routearray - username - score - journal - city
    # city - routeid - routearray - average - journal - totals - users 
    # username - routes{}
    try:
        
        route = Route.objects.get(routeid=newReview["routeid"])
        route.total += 1
        route.average = (route.average * (route.total - 1) + newReview["score"])/route.total
        print((route.average * (route.total - 1) + newReview["score"])/route.total)
        if not newReview["username"] in json.loads(route.users)["users"]:
            temp = json.loads(route.users)
            temp["users"].append(newReview["user"])
            route.users = json.dumps(temp)
        if newReview["journal"] != "":
            temp = json.loads(route.journal)
            temp["journal"].append(newReview["journal"])
            route.journal = json.dumps(temp)
        route.save()
    except:
        route =  Route(city=newReview["city"], routeid = newReview["routeid"],\
            routearray=newReview["routearray"], average=newReview["score"],
            total=1, users=json.dumps({"users":[newReview["username"]]}), \
            journal=json.dumps({"journal":[newReview["journal"]]}))
        route.save()
        
    try:
        user = User.objects.get(username=newReview["username"])
        routes = json.loads(user.routes)
        routes[newReview["routeid"]] = {"review":newReview["score"],"journal":newReview["journal"]}
        
        user.routes = json.dumps(routes)
        user.save()
    except:
        routes = {newReview["routeid"]:{"review":newReview["score"],"journal":newReview["journal"]}}
        
        user = User(username=newReview["username"],routes=json.dumps(routes))
        user.save()
    return JsonResponse({'resp': "hi"})

def get_keys(request):
    dotenv.load_dotenv()
    return JsonResponse(
        {
            "opena":os.getenv("API_KEY1"),
            "google":os.getenv("API_KEY2")
        }
    )
'''
{
    "routeid":"iosssssssssssss",
    "routearray":["l1","l2","l4"],
    "username":"mangobi",
    "score":3,
    "journal":"amazing",
    "city":"new york"
}
'''
    
