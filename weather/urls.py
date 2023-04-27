import debug_toolbar
from django.urls import path
from .views import WeatherSearchView, ClimateSearchView

urlpatterns = [
    path("", WeatherSearchView.as_view(), name='weather_search'),
    path("month/", ClimateSearchView.as_view(), name='climate_search'),
]