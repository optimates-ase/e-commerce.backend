from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ProviderAPIView.as_view(), name="provider_create"),
    path("", views.ProviderAPIView.as_view(), name="provider_read_update_delete"),
    path("rate/", views.ProviderRatingAPIView.as_view(), name="provider_rating"),
]
