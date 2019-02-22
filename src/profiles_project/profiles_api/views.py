from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from rest_framework import filters

from rest_framework.authtoken.serializers import  AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions

# Create your views here.
class HelloApiView(APIView):
    """
    Test API View
    """
    serializer_class = serializers.HelloSerializer

    def get(self,request,format = None):
        """Return a list of APIView features"""

        an_apiview = [
        'Uses HTTP methods as function (get,post,patch,put,delete)',
        'It is similar to a traditional Django view',
        'Gives you the most control over your logic',
        'Is mapped manually to URLs'
        ]

        return Response({'message' : 'Hello!','an_apiview':an_apiview})

    def post(self, request):
        """ Create a Hello Message with our name """

        serializer = serializers.HelloSerializer(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        return Response(
            serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk = None):
        """
        Handles updating an object
        """
        return Response({'method': 'put'})

    def patch(self, request, pk =None):
        """
        Patch request, only updates fields provided in the request
        """
        return Response({'method':'patch'})

    def delete(self, request, pk = None):
        """
        deletes a Object
        """
        return Response({'method' : 'delete'})

class HelloViewSet(viewsets.ViewSet):

    """ Test API ViewSets"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """ Return a Hello Message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update, destroy)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """ Create a new hello message"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
        """ Handles getting an Object by ID"""

        return Response(
            {'http_method': "GET"}
        )

    def update(self, request, pk = None):
        """Handles updating an object"""
        return Response({'http_method' : 'PUT'} )

    def partial_update(self, request, pk = None):
        """Handles updating part of an Object"""

        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk = None):
        """Handles removing an Object"""
        return Response({ 'http_request' : "DELETE"})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer

    queryset = models.UserProfile.objects.all()

    # Adding token Authentication
    authentication_classes = (TokenAuthentication,)

    # Adding permission classes

    permission_classes = (permissions.UpdateOnProfile,)

    # Adding filters

    filter_backends = (filters.SearchFilter,)

    # adding fields which should be filter

    search_fields =  ('name', 'email')

class LoginViewSet(viewsets.ViewSet):
    """check email and password and returns a auth token"""

    serializer_class = AuthTokenSerializer

    # Define a create request Post Request

    def create(self,request):
        """Use the ObtainAuthToken APIView to validate and create a token"""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed Items"""

    authentication_classes = (TokenAuthentication,)

    serializer_class = serializers.ProfileFeedItemSerializer

    # it will update delete or make if they are logged in or if not then read only
    permission_classes = (IsAuthenticatedOrReadOnly,permissions.PostOwnStatus)

    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the Logged In User"""

        serializer.save(user_profile = self.request.user)
