from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import authenticate

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
    