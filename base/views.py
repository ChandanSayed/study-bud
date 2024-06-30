from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def home(request):
  return HttpResponse('Home')

def room(request):
  template = loader.get_template('base/room.html')
  return HttpResponse(template.render())
