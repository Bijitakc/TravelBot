from django.urls import path
from . import views

# from hotel_app import views as hotel_view

urlpatterns = [
    path('hotel/', views.hotel, name='hotel'),
    path('hotel/booking/<int:id>/', views.booking, name='booking'),
    path('hotel/booking/checkout/', views.checkout, name='checkout'),
    path('booking_details/<int:id>/', views.booking_details, name='booking_details'),
]
