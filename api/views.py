from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.serializer import UserSerializer


from .serializers import OrganisationSerializer
from .models import Organisation


# Create your views here.
def using(request):
  user = User.objects.all()

  print([i.id for i in user])
  return HttpResponse(request)


class OrganisationViewSet(ModelViewSet):
  http_method_names = ['get','head','options']

  permission_classes = [IsAuthenticated]
  serializer_class = OrganisationSerializer

  def get_queryset(self):
    user= self.request.user

    queryset = Organisation.objects.filter(user=user)
    return queryset
  
  def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Organisations fetched successfully",
            "data": {
                "organisations": serializer.data
            }
        }, status=status.HTTP_200_OK)
  




class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        authenticated_user  = request.user
        if authenticated_user == user:
            serializer = self.serializer_class(user)
            response_data = {
                "status": "success",
                "message": "My details fetched successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        belogn_to_same_org = Organisation.objects.filter(user=user).filter(user=authenticated_user)
        if belogn_to_same_org.exists():
            serializer = self.serializer_class(user)
            response_data = {
                "status": "success",
                "message": "This User whose details is fetched successfully, we belong to the same organisation",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)


        
        return Response(
            {
                "status": "Bad request",
                "message": "You do not have permission to view this user record",
                "statusCode": status.HTTP_400_BAD_REQUEST
            },
            status=status.HTTP_400_BAD_REQUEST
        )
            
