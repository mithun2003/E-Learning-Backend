from django.db import models
from account.models import *
from courses.models import *
# Create your models here.
class Quiz(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=100,default='')
    option2 = models.CharField(max_length=100,default='',null=True,blank=True)
    option3 = models.CharField(max_length=100,default='',null=True,blank=True)
    option4 = models.CharField(max_length=100,default='',null=True,blank=True)
    correct_answer = models.CharField(max_length=100)
    answer_type = models.CharField(max_length=10, default='checkbox')
# class QuizKey(models.Model):
#     course = models.ForeignKey(Course)
class QuizAttempt(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    attempt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.question}"