from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from . import serializers

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

    def list(self, request):
        """ Return a Hello Message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update, destroy)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})
