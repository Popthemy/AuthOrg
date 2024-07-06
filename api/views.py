from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import User

# Create your views here.
def using(request):
  user = User.objects.all()

  print([i.id for i in user])
  return HttpResponse(request)