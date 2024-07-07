from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('', views.Home, name='home'),
    path('room-details/<int:pk>/', views.GetRoom, name='room-details'),
    path('create-room/',views.CreateRoom, name='create-room'),
    path('update-room/<int:pk>/',views.UpdateRoom, name='update-room'),
    path('delete-room/<int:pk>/',views.DeleteRoom, name='delete-room'),
    ]