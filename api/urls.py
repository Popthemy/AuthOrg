from django.urls import path
from .views import using

urlpatterns = [
    path('',using)
]
