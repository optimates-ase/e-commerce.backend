from django.urls import path
from .views import ImageAPIView

urlpatterns = [
    path("get/", ImageAPIView.as_view(), name="image"),
]
