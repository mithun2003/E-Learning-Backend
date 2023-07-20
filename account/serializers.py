from djoser.email import ActivationEmail, ConfirmationEmail
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    ActivationSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from djoser import utils
from django.conf import settings as djangosettings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from django.utils import timezone
import random
import string
import pyotp
import hashlib
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.validators import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "You are not authorized to perform this action"
                    )
                else:
                    data["user"] = user
            else:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Email and Password are required")
        return data


class UserCreateSerializer(UserCreateSerializer):
    image = serializers.ImageField(required=False)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "name", "email", "image", "password")


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, user):
        if user.image:
            image_url = user.image.url
            if image_url.startswith("/media/media"):
                image_url = image_url.replace("/media/media", "/media")
            return image_url
        else:
            return None

    class Meta:
        model = UserAccount
        exclude = ("password",)


class TeacherCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())

    class Meta:
        model = Teachers
        fields = ("user", "address", "highest_qualification", "skills", "resume")


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teachers
        fields = (
            "user",
            "highest_qualification",
            "skills",
            "address",
            "resume",
        )


class CustomActivationEmail(ActivationEmail):
    template_name = "activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        print(context)
        user = context.get("user")
        key = User.objects.get(email=user.email).id
        print(key)
        hashed_user_id = hashlib.sha256(str(key).encode("utf-8")).hexdigest()

        # Set the seed for the random number generator based on the hashed user ID
        random.seed(hashed_user_id)

        # Generate a random string of characters for the secret key
        secret_key = "".join(random.choices(string.ascii_uppercase + "234567", k=16))
        # Create a TOTP object with a 30 second interval
        totp = pyotp.TOTP(secret_key, interval=600)
        print(secret_key, key)

        # Generate an OTP
        otp = totp.now()

        print(secret_key)
        context["name"] = "E-Learning"
        context["msg"] = "OTP VERIFICATION"
        context["otp"] = otp
        # context['domain'] = djangosettings.FRONT_END
        # context["uid"] = utils.encode_uid(user.pk)
        # context["token"] = default_token_generator.make_token(user)
        # context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


class ConfirmationEmail(ConfirmationEmail):
    template_name = "ConfirmationEmail.html"


class ActivationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    user_id = serializers.IntegerField()

    # uid = serializers.CharField(required=False)
    # token = serializers.CharField(required=False)
    def validate(self, attrs):
        attrs = super().validate(attrs)
        print(attrs)
        user_id = attrs.get("user_id")
        print(user_id)
        self.user = UserAccount.objects.get(id=user_id)
        return attrs
