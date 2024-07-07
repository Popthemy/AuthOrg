from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.serializer import UserSerializer


from .serializers import OrganisationSerializer,AddUserToOrganisationSerializer
from .models import Organisation


class AddRetrieveUserOrganisationViewSet(ViewSet):
    serializer_class = AddUserToOrganisationSerializer

    def create(self, request, organisation_pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve organisation
        try:
            organisation = Organisation.objects.get(pk=organisation_pk)
        except Organisation.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Organisation not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Retrieve user
        id = serializer.validated_data['userId']
        try:
            user = User.objects.get(id=id)
            organisation.user.add(user)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Add user to organisation
        organisation.user.add(user)

        return Response({
            "status": "success",
            "message": "User added to organisation successfully"
        }, status=status.HTTP_201_CREATED)
    

    def retrieve(self, request, organisation_pk=None):
        try:
            organisation = Organisation.objects.get(pk=organisation_pk)
        except Organisation.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Organisation not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all users belonging to this organisation
        users_in_organisation = organisation.user.all()

        # Check if the requesting user belongs to this organisation
        if not request.user in organisation.user.all():
            return Response({
                "status": "error",
                "message": "You do not have permission to access this organisation"
            }, status=status.HTTP_403_FORBIDDEN)

        

        # Serialize users and prepare response
        users_serializer = UserSerializer(users_in_organisation, many=True)
        
        return Response({
            "status": "success",
            "message": "Users in organisation fetched successfully",
            "data": {
                "users_in_organisation": users_serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    def list(self, request, organisation_pk=None):
        try:
            organisation = Organisation.objects.get(pk=organisation_pk)
        except Organisation.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Organisation not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all users belonging to this organisation
        users_in_organisation = organisation.user.all()


        # Check if the requesting user belongs to this organisation
        if not request.user in users_in_organisation:
            return Response({
                "status": "error",
                "message": "You do not have permission to access this organisation's users"
            }, status=status.HTTP_403_FORBIDDEN)

        
        # Serialize users and prepare response
        users_serializer = UserSerializer(users_in_organisation, many=True)
        
        return Response({
            "status": "success",
            "message": "Users in organisation fetched successfully",
            "data": {
                "users_in_organisation": users_serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    



class OrganisationViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']

    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        user = self.request.user

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
    

    def retrieve(self, request, pk=None):
         if pk:
            org = Organisation.objects.filter(pk=pk)
            if org.exists():

                if org.filter(user=request.user).exists():

                    org = Organisation.objects.get(pk=pk)
                    
                    serializer = self.serializer_class(org)

                    return Response({
                        "status": "success",
                        "message": "Organisation fetched successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                
                else:
                    return Response({
                        "status": "error",
                        "message": "You do not have permission to access this organisation"
                    }, status=status.HTTP_403_FORBIDDEN)
                

            else:
                return Response({
                    "status": "error",
                    "message": "Organisation doesn't exist"
                }, status=status.HTTP_404_NOT_FOUND)
            

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            org = serializer.save()

            return Response({
                            "status": "success",
                            "message": "Organisation created successfully",
                            "data":serializer.data
                            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "Bad request",
            "message": "Client error",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        authenticated_user = request.user
        if authenticated_user == user:
            serializer = self.serializer_class(user)
            response_data = {
                "status": "success",
                "message": "My details fetched successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        belong_to_same_org = Organisation.objects.filter(
            user=user).filter(user=authenticated_user)

        if belong_to_same_org.exists():
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
