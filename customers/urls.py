from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CustomerAPIView.as_view(), name='customer_create'),
    path('', views.CustomerAPIView.as_view(), name='customer_read_update_delete'),
    path('mark-tour/', views.CustomerMarkingTourAPIView.as_view(), name='mark_tour'),
    path('book-tour/', views.CustomerBookingTourAPIView.as_view(), name='book_tour'),
    path('mark-tour/all', views.CustomerMarkingTourAllAPIView.as_view(), name='marked_tours'),
    path('book-tour/all', views.CustomerBookingTourAllAPIView.as_view(), name='booked_tours'),
]
