from djoser.email import ActivationEmail,ConfirmationEmail
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from djoser import utils
from django.conf import settings as djangosettings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email', 'password')
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, user):
        if user.image:
            image_url = user.image.url
            if image_url.startswith('/media/media'):
                image_url = image_url.replace('/media/media', '/media')
            return image_url
        else:
            return None
    class Meta:
        model = UserAccount
        fields = "__all__"    
# class TeacherCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teachers
#         fields = ('id', 'name', 'email', 'image','country','mobile_number','address','highest_qualification','skills','resume')
class TeacherCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    class Meta:
        model = Teachers
        fields = ( 'user', 'address', 'highest_qualification', 'skills', 'resume')
# class UserSerializerDjoser(UserSerializer):
#     class Meta(UserSerializer.Meta):
#         model = User
#         fields = (
#             "id",
#             "name",
#             "email",
#             "is_active",
#             "is_block",
#             'is_student'
#         )



# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teachers
#         fields = (
#             "name",
#             "email",
#             "highest_qualification",
#             "skills",
#             'address',
#             'image',
#             'country',
#             'mobile_number',
#             'resume',
#             'is_block',
#             'is_verified'
#         )
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teachers
        fields = (
            "user",
            "highest_qualification",
            "skills",
            'address',
            'resume',
        )


class CustomActivationEmail(ActivationEmail):
    template_name = "activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        context['name'] = 'E-Learning'
        context['domain'] = djangosettings.FRONT_END
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context

class ConfirmationEmail(ConfirmationEmail):
    template_name = 'ConfirmationEmail.html'