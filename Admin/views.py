from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from account.serializers import *
from account.models import Teachers
from courses.models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.models import *

class Admin_Panel(APIView):
    def get(self,request):
        enrollments=Enrollment.objects.all().count()
        teacher = Teachers.objects.filter(user__is_staff=False,user__is_teacher=True).count()
        users = UserAccount.objects.filter(is_staff=False,is_teacher=False).count()
        courses = Course.objects.all().count()
        return Response({"data":enrollments,"teacher":teacher,"user":users,"course":courses})
# class Total_Teachers(APIView):
#     def get(self,request):
#         return Response({})
# class Total_Users(APIView):
#     def get(self,request):
#         return Response({})
# class Total_Courses(APIView):
#     def get(self,request):
#         return Response({})
    