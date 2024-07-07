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


class AddUserToOrganisationViewSet(ViewSet):
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

# class AddUserToOrganisationViewSet(ModelViewSet):
#     http_method_names = ['POST','HEAD','OPTIONS']
#     serializer_class = AddUserToOrganisationSerializer

#     def get_queryset(self):
#         organisation_id = self.kwargs['organisation_pk']
#         return User.objects.filter(organisations__org_id=organisation_id)
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         organisation = serializer.save()

#         return Response({
#             "status": "success",
#             "message": "User added to organisation successfully"
#         }, status=status.HTTP_201_CREATED)



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

    def retreive(self, request, pk=None):
        if pk:
            if Organisation.objects.filter(pk=pk).filter(user=request.user).exists():

                org = Organisation.objects.get(pk=pk)
                print(org)
                serializer = self.serializer_class(org)

                return Response({
                    "status": "success",
                    "message": "Organisation fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    "status": "error",
                    "message": "Organisation not found or you do not have permission to access this organisation"
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
                            }, status=status.HTTP_404_NOT_FOUND)
        
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
