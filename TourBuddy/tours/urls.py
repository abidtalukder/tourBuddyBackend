# tours/urls.py
from django.urls import path
from .views import TourListCreateView, TourDetailView, LandmarkListCreateView, LandmarkDetailView

urlpatterns = [
    # path('', views.tourList, name='tourList'),
    # path('<int:tour_id>/', views.tourDetail, name='tourDetail'),
    path('tours/', TourListCreateView.as_view(), name='tour-list-create'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('locations/', LandmarkListCreateView.as_view(), name='landmark-list-create'),
    path('locations/<int:pk>/', LandmarkDetailView.as_view(), name='landmark-detail'),
]
