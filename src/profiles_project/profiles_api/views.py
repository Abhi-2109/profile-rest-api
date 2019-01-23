from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
