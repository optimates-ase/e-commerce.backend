from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.TourAPIView.as_view(), name="tour_create"),
    path("", views.TourAPIView.as_view(), name="tour_read_update_delete"),
    path("randomize/", views.RandomToursAPIView.as_view(), name="tour_random"),
    path("rate/", views.TourRatingAPIView.as_view(), name="tour_rating"),
]
