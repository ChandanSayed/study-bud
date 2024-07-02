from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room-details/<int:pk>/', views.room, name='room-details'),
    ]