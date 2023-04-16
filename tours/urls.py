from django.urls import path
from . import views

urlpatterns = [
    path('', views.TourAPIView.as_view(), name='tour_create'),
    path('<int:pk>/', views.TourAPIView.as_view(), name='tour_rud'),
    path('random/', views.RandomTourAPIView.as_view(), name="tour_random"),
]
