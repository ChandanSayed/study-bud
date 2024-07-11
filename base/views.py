from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q 
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def LoginPage(request):
  page = 'login'
  if request.user.is_authenticated:
        return redirect('home')
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      user = User.objects.get(username=username)
      
    except:
      messages.error(request,'User does not exist')
      return redirect('login')
    
    user = authenticate(request,username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request,'Username or password is incorrect')

  context = {'page':page}
  return render(request, 'base/login_register.html',context)

def RegisterPage(request):
  form = UserCreationForm()
  if request.user.is_authenticated:
        return redirect('home')
  context = {'form':form}
  return render(request, 'base/login_register.html',context)

def LogoutUser(request):
  logout(request)
  return redirect('home')

def Home(request):
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

def GetRoom(request,pk):
  room = Room.objects.get(id=pk)
  context = {
    'room': room,
  }
  template = loader.get_template('base/room.html')
  return HttpResponse(template.render(context,request))

@login_required(login_url='login')
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

@login_required(login_url='login')
def UpdateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)

  if request.user != room.host:
    messages.error(request,'You are not allowed to do this!')
    return redirect('home')

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')
  context = {'form':form}
  return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def DeleteRoom(request,pk):
  room = Room.objects.get(id=pk)
  if request.user != room.host:
    messages.error(request,'You are not allowed to do this!')
    return redirect('home')
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request,'base/room_delete.html',{'obj':room})
