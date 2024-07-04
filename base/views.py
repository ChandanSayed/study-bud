from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q 
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.


def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains = q)
    | Q(name__icontains = q )|
    Q(description__icontains = q )
    ).order_by('-updated','-created')
  room_count = rooms.count()
  topics = Topic.objects.all()
  context = {
    'all_rooms': rooms,
    'all_topics': topics,
    'room_count': room_count
  }
  template = loader.get_template('base/home.html')
  return HttpResponse(template.render(context,request))

def room(request,pk):
  room = Room.objects.get(id=pk)
  context = {
    'room': room,
  }
  template = loader.get_template('base/room.html')
  return HttpResponse(template.render(context,request))

def CreateRoom(request):
  # template = loader.get_template('base/room_form.html')
  form = RoomForm() 
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  context ={'form':form}
  return render(request,'base/room_form.html',context)


def UpdateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'base/room_form.html',context)


def DeleteRoom(request,pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request,'base/room_delete.html',{'obj':room})
