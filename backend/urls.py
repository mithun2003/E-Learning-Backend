from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from account.views import AdminLoginView
from courses.views import ContactMe, Banner,EditBanner,BannerUser
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
# import chat.routing
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    # path('social/', include('allauth.urls')),
    
    path('admin_view/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('account.urls')),
    path('course/', include('courses.urls')),
    path('course/', include('quiz.urls')),
    path('contact/', ContactMe.as_view()),
    path('banner/', Banner.as_view()),
    path('banner/user', BannerUser.as_view()),
    path('banner/<id>', EditBanner.as_view()),
    
    
    
    path('chat/', include('chat.urls')),
    
    
    path('live/', include('live.urls')),


    path('admin/',include('Admin.urls'))
    

]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn
# sudo systemctl restart gunicorn.socket gunicorn.service
# sudo nginx -t && sudo systemctl restart nginx