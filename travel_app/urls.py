from django.urls import path
from .views import PlaceDetailView
from . import views
from hotel_app import views as hotel_view

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('destination/', views.destination, name='destination'),
    path('hotel/', hotel_view.hotel, name='hotel'),
    path('search/', views.search, name='search'),
    path('detail/<int:pk>/', PlaceDetailView.as_view(), name='detail'),
]


