from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Room
# Create your views here.


def home(request):
  rooms = Room.objects.all()
  print(rooms)
  context = {
    'all_rooms': rooms,
  }
  template = loader.get_template('base/home.html')
  return HttpResponse(template.render(context,request))

def room(request,pk):
  room = Room.objects.get(id=pk)
  print()
  context = {
    'room': room,
  }
  template = loader.get_template('base/room.html')
  return HttpResponse(template.render(context,request))
