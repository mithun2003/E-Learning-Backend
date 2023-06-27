from django.urls import path
from .views import *


urlpatterns = [
    path('admin_panel', Admin_Panel.as_view()),
    # path('total_users', Total_Users.as_view()),
    # path('total_teachers', Total_Teachers.as_view()),
    # path('total_courses', Total_Courses.as_view()),
   
]
