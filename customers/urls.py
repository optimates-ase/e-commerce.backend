from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CustomerAPIView.as_view(), name='customer_create'),
    path('', views.CustomerAPIView.as_view(), name='customer_read_update_delete'),
]
