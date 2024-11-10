from django.db import models

# Create your models here.

# Location model for storing the name and description. Landmarks include
# businesses, parks, restaurants, and other points of interest.
class Landmark(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    latitude = models.FloatField(default = 0.0)
    longitude = models.FloatField(default = 0.0)

    def __str__(self):
        return self.name
    
# Tour model for storing the title of a tour as well as the landmarks that are
# part of the tour.
class Tour(models.Model):
    title = models.CharField(max_length=100)
    landmarks = models.ManyToManyField(Landmark)

    def __str__(self):
        return self.title

class Route(models.Model):
    # city - routeid - routename - average - entries - totals - users 
    city = models.CharField(max_length=255)
    routeid = models.CharField(max_length=2048)
    routearray = models.JSONField()
    average = models.FloatField()
    total = models.IntegerField()
    journal = models.JSONField()
    users = models.JSONField()
class User(models.Model):
    username = models.CharField(max_length=255)
    routes = models.JSONField()
class Location(models.Model):
    #id = models.IntegerField()
    city = models.CharField(max_length=255)
    rating = models.FloatField()
    total = models.IntegerField()
    users = models.JSONField()
    journal = models.JSONField()