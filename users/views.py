from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def user_profile(request):
   return render (request, 'home.html')


