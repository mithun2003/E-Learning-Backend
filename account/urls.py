from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('super/login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    
    
    path('get/users/', RetrieveUserView.as_view()),
    path('user/', GetOneUser.as_view()),
    path('view/user/<user_id>', ViewOneUser.as_view()),
    path('user/delete/<id>', DeleteUser.as_view()),
    path('user/block/<id>', BlockUser.as_view()),
    path('user/edit/<id>', EditUser.as_view()),
    path('auth/user/login/', Login.as_view(), name='custom_login'),
    
    
    
    
    path('teacher/register', Teacher.as_view()),
    path('request/teacher/verify/<id>', Verify.as_view()),
    path('request/teacher/reject/<id>', Reject.as_view()),
    path('teacher/get', RetrieveTeacherView.as_view()),
    path('teacher/get/<id>', RetrieveOneTeacherView.as_view()),
    path('request/teacher/<id>', OneTeacher.as_view()),
    path('request/teacher/', RequestTeacher.as_view()),
    # path('teacher/block/<id>', BlockTeacher.as_view()),

    # path('get/users/', get_users),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)