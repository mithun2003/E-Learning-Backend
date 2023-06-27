from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [
    path('quiz/',QuizView.as_view()),
    path('quiz/attempt/<course_id>',QuizAttemptAPIView.as_view())
]