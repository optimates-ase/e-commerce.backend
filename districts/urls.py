import debug_toolbar
from django.urls import path
from .views import DistrictCreateView, DistrictSearchView

urlpatterns = [
    path("create/", DistrictCreateView.as_view(), name='district_create'),
    path("search/", DistrictSearchView.as_view(), name='district_search'),
]