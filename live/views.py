from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from .serializer import *


class LiveView(APIView):
    def post(self, request):
        serializer = LiveCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = Live.objects.all().order_by('-created_at')
        if queryset:
            serializer = LiveSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class DeleteLive(APIView):  
    def delete(self,request,room_code):
        # room_code = request.data.get('room_code')
        print(room_code)
        live = Live.objects.get(room_code=room_code)
        live.delete()
        return Response({'message': 'Course removed from live'})
