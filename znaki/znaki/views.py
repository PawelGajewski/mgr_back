from django.http import HttpResponse
from .serializers import znakserializer, userserializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Znak
from .serializers import znakserializer
from rest_framework.decorators import api_view


#@api_view(['GET', 'POST'])
class znak(APIView):
    def get(self, request):
        znaki = Znak.objects.all().order_by('id')
        serializer = znakserializer(znaki, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = znakserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class znaksingle(APIView):
    def get(self, request, pk):
        znak = Znak.objects.get(pk=pk)
        serializer = znakserializer(znak)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        znak = Znak.objects.get(pk=pk)
        serializer = znakserializer(znak, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
