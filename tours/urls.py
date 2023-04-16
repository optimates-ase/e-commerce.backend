from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TourAPIView.as_view(), name='tour_create'),
    path('<int:pk>/', views.TourAPIView.as_view(), name='tour_read_update_delete'),
    path('random/', views.RandomTourAPIView.as_view(), name="tour_random"),
]
