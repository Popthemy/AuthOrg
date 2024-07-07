from django.urls import path,include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('organisations',views.OrganisationViewSet,basename='organisations')


urlpatterns = [
    path('',views.using),
    path('',include(router.urls)),
    path('users/<str:pk>/', views.UserDetails.as_view(), name='user-organisation-details'),

]
