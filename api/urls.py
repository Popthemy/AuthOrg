from django.urls import path,include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('organisations',views.OrganisationViewSet,basename='organisation')

organisation_router = routers.NestedDefaultRouter(router, 'organisations', lookup='organisation')
organisation_router.register('users', views.AddUserToOrganisationViewSet, basename='organisation-users')


urlpatterns = [
    path('',include(router.urls)),
    path('users/<str:pk>/', views.UserDetails.as_view(), name='user-organisation-details'),
    path('',include(organisation_router.urls))

]
