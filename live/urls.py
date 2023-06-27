from django.urls import path
from .views import *


urlpatterns = [
    path('', LiveView.as_view(), name='live'),
    path('<room_code>',DeleteLive.as_view())
]
