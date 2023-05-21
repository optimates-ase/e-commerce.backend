import debug_toolbar
from django.urls import path
from .views import GeoDistrictsSearchView, GeoSearchView

urlpatterns = [
    path("belize/", GeoSearchView.as_view(), name='district_create'),
    path("districts/", GeoDistrictsSearchView.as_view(), name='district_search'),
]