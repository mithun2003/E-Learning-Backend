from django.db import models
from account.models import *
from chat.models import *


# Create your models here.
class Banners(models.Model):
    image = models.ImageField(upload_to='banner/')
    title = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    is_publish = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class Course(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    image = models.ImageField(upload_to='course/', blank=False, null=False)
    desc = models.TextField()
    cat = models.ManyToManyField(Category)
    # enrollments = models.PositiveIntegerField(default=0)
    duration = models.DurationField()
    level = models.CharField(max_length=15)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    is_publish = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



    def enrollments(self):
        print(self)
        enrollments = Enrollment.objects.filter(course=self).count()
        return enrollments

    def avg_rating(self):
        avg_rating = CourseReview.objects.filter(course=self).aggregate(models.Avg('rating'))
        avg_rating_value = avg_rating['rating__avg']
        if avg_rating_value is not None:
            avg_rating_formatted = "{:.2f}".format(avg_rating_value)
            return avg_rating_formatted
        return None
    def __str__(self):
        return self.title
    

class Chapter(models.Model):
    title = models.CharField(max_length=100, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    order = models.PositiveIntegerField()
    video = models.FileField(upload_to='chapter_videos/', blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def completed(self, user):
        try:
            is_completed = VideoProgress.objects.get(video=self, course=self.course, user=user)
            return is_completed.is_completed
        except VideoProgress.DoesNotExist:
            return False

    class Meta:
        ordering = ['order']


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    enrolled_at = models.DateField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    review = models.TextField()
    rating_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateField(auto_now_add=True)


class VideoProgress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)


class CourseProgress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)


