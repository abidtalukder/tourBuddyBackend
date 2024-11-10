# tours/urls.py
from django.urls import path
from .views import TourListCreateView, TourDetailView, LocationListCreateView, LocationDetailView

urlpatterns = [
    # path('', views.tourList, name='tourList'),
    # path('<int:tour_id>/', views.tourDetail, name='tourDetail'),
    path('tours/', TourListCreateView.as_view(), name='tour-list-create'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
]
