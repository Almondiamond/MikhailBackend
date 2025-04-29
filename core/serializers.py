from typing import Any

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, User
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    permissions = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def get_profile_id(self, obj):
        return Profile.objects.get(user__id=obj.id).id

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'


class UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['pic']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user = get_user_model().objects.get(id=decoded_payload['user_id'])
        refresh = RefreshToken.for_user(user)
        return {
            'access': data['access'],
            'refresh': str(refresh),
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        print('arrts', attrs)
        user = authenticate(**attrs)
        if user is None:
            raise exceptions.NotFound('Пользователь не найден')

        return super().validate(attrs)



class CreateOfferSerializer(serializers.Serializer):
    offer_id = serializers.CharField()