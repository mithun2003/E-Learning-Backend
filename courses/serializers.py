from djoser.serializers import UserSerializer
from rest_framework import serializers
from .models import *
from account.serializers import *
from chat.models import ChatRoom
from django.conf import settings


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
            if obj.image:
                if settings.DEBUG:
                    return "http://localhost:8000" + obj.image.url
                else:
                    return "https://studypoint.shop" + obj.image.url
            else:
                return None

    class Meta:
        model = Banners
        fields = ('id', 'title', 'image', 'created_at', 'active')


class CreateBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = ('title', 'image')


class CategoryCreateSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'is_publish')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'created_at',
            'is_publish'
        )


class CourseCreateSerializer(serializers.ModelSerializer):
    print(serializers.ModelSerializer)
    chat_room = serializers.SerializerMethodField()

    def get_chat_room(self, course):
        teacher = course.teacher
        chat_room, created = ChatRoom.objects.get_or_create(name=course.title)
        if created:
            chat_room.users.add(teacher.user.id)
        return chat_room.id

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'image',
            'desc',
            'cat',
            'enrollments',
            'duration',
            'level',
            'teacher',
            'is_publish',
            'chat_room'
        )


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()  # serialize the related teacher data
    cat = CategorySerializer(many=True)  # serialize the related category data
    image = serializers.SerializerMethodField()
    chat_room = serializers.SerializerMethodField()

    def get_chat_room(self, course):
        chat_room_name = course.title
        chat_room = ChatRoom.objects.filter(name=chat_room_name).first()
        chat_room_id = chat_room.id if chat_room else None
        return chat_room_id


    def get_image(self, obj):
            if obj.image:
                if settings.DEBUG:
                    return "http://localhost:8000" + obj.image.url
                else:
                    return "https://studypoint.shop" + obj.image.url
            else:
                return None

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('id',
                  'title',
                  'image',
                  'desc',
                  'cat',
                  'enrollments',
                  'duration',
                  'level',
                  'teacher',
                  'is_publish',
                  'avg_rating',
                  'created_at',
                  'chat_room'
                  )


class ChapterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'title', 'video', 'order', 'course')


class ChapterSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    def get_video(self, obj):
        if obj.video:
            if settings.DEBUG:
                return "http://localhost:8000" + obj.video.url
            else:
                return "https://studypoint.shop" + obj.video.url
        else:
            return None

    def get_completed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:

            return obj.completed(user)
        else:
            return None

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'course', 'order', 'video', 'completed')


class AdminChapterSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    def get_video(self, obj):
        if obj.video:
            if settings.DEBUG:
                return "http://localhost:8000" + obj.video.url
            else:
                return "https://studypoint.shop" + obj.video.url
        else:
            return None

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'course', 'order', 'video')


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Enrollment
        fields = '__all__'


class WishlistCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ('user', 'courses')


class WishlistSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ('user', 'course')

class UserWishlistSerializer(serializers.ModelSerializer):
    # course = CourseSerializer()
    course = CourseSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ('course',)


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested serializer for the course field
    user = UserSerializer()

    class Meta:
        model = CourseReview
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message', 'sent_at')


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ('user', 'course', 'video', 'is_completed')


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ('user', 'course', 'progress')


