import debug_toolbar
from django.urls import path
from .views import DistrictCreateView

urlpatterns = [
    path("create/", DistrictCreateView.as_view(), name='district_create'),
]