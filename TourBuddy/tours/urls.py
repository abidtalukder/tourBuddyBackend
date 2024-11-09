# tours/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tourList, name='tourList'),
    path('<int:tour_id>/', views.tourDetail, name='tourDetail'),
]
