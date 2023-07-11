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
    image = serializers.ImageField(required=False)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'name', 'email','image', 'password')
        # fields = '__all__'
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
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
        # fields = "__all__"    
        exclude = ('password',)

class TeacherCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    class Meta:
        model = Teachers
        fields = ( 'user', 'address', 'highest_qualification', 'skills', 'resume')





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